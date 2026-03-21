import copy
from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ECO, ECOProposedChange
from .serializers import ECOSerializer, ECODetailSerializer
from apps.settings_app.models import ECOStage
from apps.approvals.models import ApprovalConfig, ApprovalRecord
from apps.users.permissions import IsEngineeringOrAdmin, IsApproverOrAdmin
from apps.audit.utils import log_event
from apps.products.models import Product
from apps.bom.models import BOM, BOMComponent, BOMOperation


# ─── Helpers ──────────────────────────────────────────────────────────────────

def apply_eco(eco, user):
    """
    Core function: applies all proposed changes when ECO reaches Done stage.
    If version_update=True: clones the record, increments version, archives old.
    If version_update=False: applies changes in place.
    """
    with transaction.atomic():
        changes = ECOProposedChange.objects.filter(eco=eco)

        if eco.version_update:
            if eco.eco_type == 'product':
                old_product = eco.product
                # Clone the product
                new_product = Product(
                    name=old_product.name,
                    sales_price=old_product.sales_price,
                    cost_price=old_product.cost_price,
                    version=old_product.version + 1,
                    status='active',
                )
                # Apply proposed field changes to clone
                for change in changes.filter(entity_type='product'):
                    if hasattr(new_product, change.field_name):
                        setattr(new_product, change.field_name, change.new_value)
                new_product.save()
                
                # Clone Attachments
                from apps.products.models import ProductAttachment
                for att in old_product.attachments.all():
                    ProductAttachment.objects.create(
                        product=new_product,
                        file_name=att.file_name,
                        file_path=att.file_path
                    )
                    
                # Clone BOMs
                for old_p_bom in old_product.boms.filter(status='active'):
                    new_p_bom = BOM(
                        product=new_product,
                        reference=old_p_bom.reference,
                        quantity=old_p_bom.quantity,
                        unit=old_p_bom.unit,
                        version=old_p_bom.version + 1,
                        status='active',
                    )
                    new_p_bom.save()
                    for comp in old_p_bom.components.all():
                        BOMComponent.objects.create(
                            bom=new_p_bom, component_product=comp.component_product,
                            quantity=comp.quantity, unit=comp.unit
                        )
                    for op in old_p_bom.operations.all():
                        BOMOperation.objects.create(
                            bom=new_p_bom, work_center=op.work_center,
                            expected_duration_mins=op.expected_duration_mins
                        )
                    BOM.objects.filter(pk=old_p_bom.pk).update(status='archived')

                # Archive old
                old_product.status = 'archived'
                Product.objects.filter(pk=old_product.pk).update(status='archived')
                log_event('version_created', 'product', new_product.id, user=user,
                          new_value=str(new_product.version))

            elif eco.eco_type == 'bom' and eco.bom:
                old_bom = eco.bom
                # Clone BOM
                new_bom = BOM(
                    product=old_bom.product,
                    reference=old_bom.reference,
                    quantity=old_bom.quantity,
                    unit=old_bom.unit,
                    version=old_bom.version + 1,
                    status='active',
                )
                new_bom.save()  # auto-generates reference
                # Clone components
                for comp in old_bom.components.all():
                    qty = comp.quantity
                    for change in changes.filter(entity_type='bomcomponent'):
                        if change.field_name == str(comp.component_product.id) or change.field_name == comp.component_product.name:
                            try:
                                from decimal import Decimal
                                qty = Decimal(str(change.new_value))
                            except Exception:
                                qty = comp.quantity

                    BOMComponent.objects.create(
                        bom=new_bom, component_product=comp.component_product,
                        quantity=qty, unit=comp.unit
                    )
                # Clone operations
                for op in old_bom.operations.all():
                    BOMOperation.objects.create(
                        bom=new_bom, work_center=op.work_center,
                        expected_duration_mins=op.expected_duration_mins
                    )
                # Apply proposed changes to new BOM clone
                for change in changes.filter(entity_type='bom'):
                    if hasattr(new_bom, change.field_name):
                        setattr(new_bom, change.field_name, change.new_value)
                new_bom.save()
                # Archive old BOM
                BOM.objects.filter(pk=old_bom.pk).update(status='archived')
                log_event('version_created', 'bom', new_bom.id, user=user,
                          new_value=str(new_bom.version))
        else:
            # Apply changes in place (no version increment)
            if eco.eco_type == 'product':
                for change in changes.filter(entity_type='product'):
                    if hasattr(eco.product, change.field_name):
                        setattr(eco.product, change.field_name, change.new_value)
                eco.product.save()
            elif eco.eco_type == 'bom' and eco.bom:
                for change in changes.filter(entity_type='bom'):
                    if hasattr(eco.bom, change.field_name):
                        setattr(eco.bom, change.field_name, change.new_value)
                eco.bom.save()
                
                for comp in eco.bom.components.all():
                    for change in changes.filter(entity_type='bomcomponent'):
                        if change.field_name == str(comp.component_product.id) or change.field_name == comp.component_product.name:
                            try:
                                from decimal import Decimal
                                comp.quantity = Decimal(str(change.new_value))
                            except Exception:
                                pass
                            comp.save()

        # Finalize ECO
        eco.status = 'applied'
        eco.effective_date = timezone.now()
        eco.save()
        log_event('data_changed', 'eco', eco.id, user=user, new_value='applied')


def get_next_stage(current_stage):
    return ECOStage.objects.filter(sequence__gt=current_stage.sequence).order_by('sequence').first()


# ─── Views ────────────────────────────────────────────────────────────────────

class ECOListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsEngineeringOrAdmin()]
        return [IsAuthenticated()]

    def get(self, request):
        qs = ECO.objects.select_related('product', 'stage', 'user').order_by('-created_at')
        return Response(ECOSerializer(qs, many=True).data)

    def post(self, request):
        # Default stage = New
        new_stage = ECOStage.objects.filter(is_default_new=True).first()
        if not new_stage:
            return Response({'error': 'Default New stage not configured. Run seed first.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = request.data.copy()
        serializer = ECOSerializer(data=data)
        if serializer.is_valid():
            eco = serializer.save(user=request.user, stage=new_stage, status='draft')
            log_event('eco_created', 'eco', eco.id, user=request.user, new_value=eco.title)
            return Response(ECODetailSerializer(eco).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ECODetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsEngineeringOrAdmin()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return ECO.objects.get(pk=pk)
        except ECO.DoesNotExist:
            return None

    def get(self, request, pk):
        eco = self.get_object(pk)
        if not eco:
            return Response({'error': 'ECO not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ECODetailSerializer(eco).data)

    def patch(self, request, pk):
        eco = self.get_object(pk)
        if not eco:
            return Response({'error': 'ECO not found'}, status=status.HTTP_404_NOT_FOUND)
        if eco.status != 'draft':
            return Response({'error': 'Only draft ECOs can be edited.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ECOSerializer(eco, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            eco.refresh_from_db()
            return Response(ECODetailSerializer(eco).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ECOStartView(APIView):
    permission_classes = [IsEngineeringOrAdmin]

    def post(self, request, pk):
        try:
            eco = ECO.objects.get(pk=pk)
        except ECO.DoesNotExist:
            return Response({'error': 'ECO not found'}, status=status.HTTP_404_NOT_FOUND)
        if eco.status != 'draft':
            return Response({'error': 'ECO is already started.'}, status=status.HTTP_400_BAD_REQUEST)
        if not eco.title or not eco.eco_type or not eco.product:
            return Response({'error': 'Fill all required fields before starting.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if eco.eco_type == 'bom' and not eco.bom:
            return Response({'error': 'BOM is required for ECO Type = BOM.'},
                            status=status.HTTP_400_BAD_REQUEST)
        eco.status = 'active'
        eco.save()
        log_event('stage_transition', 'eco', eco.id, user=request.user,
                  new_value=eco.stage.name)
        return Response(ECODetailSerializer(eco).data)


class ECOValidateView(APIView):
    """Advance stage — used when no Required approver configured (any user can click)."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            eco = ECO.objects.get(pk=pk)
        except ECO.DoesNotExist:
            return Response({'error': 'ECO not found'}, status=status.HTTP_404_NOT_FOUND)
        if eco.status != 'active':
            return Response({'error': 'ECO is not active.'}, status=status.HTTP_400_BAD_REQUEST)

        # Bug 3 Fix: Only the ECO owner or an Admin should be able to manually skip/advance
        if request.user != eco.user and not request.user.is_staff and request.user.role != 'admin':
            return Response(
                {'error': 'Only the ECO creator or an Admin can manually validate this stage.'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Check all required approvals are done for current stage
        required_configs = ApprovalConfig.objects.filter(stage=eco.stage, category='required')
        for config in required_configs:
            if not ApprovalRecord.objects.filter(eco=eco, stage=eco.stage, user=config.user).exists():
                return Response(
                    {'error': f'Required approval from {config.user.login_id} is still pending.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        next_stage = get_next_stage(eco.stage)
        if not next_stage:
            return Response({'error': 'Already at the final stage.'}, status=status.HTTP_400_BAD_REQUEST)

        eco.stage = next_stage
        eco.save()
        log_event('stage_transition', 'eco', eco.id, user=request.user, new_value=next_stage.name)

        if next_stage.is_default_done:
            apply_eco(eco, request.user)
            eco.refresh_from_db()

        return Response(ECODetailSerializer(eco).data)


class ECOApproveView(APIView):
    """Designated approver approves the ECO at the current stage."""
    permission_classes = [IsApproverOrAdmin]

    def post(self, request, pk):
        try:
            eco = ECO.objects.get(pk=pk)
        except ECO.DoesNotExist:
            return Response({'error': 'ECO not found'}, status=status.HTTP_404_NOT_FOUND)
        if eco.status != 'active':
            return Response({'error': 'ECO is not active.'}, status=status.HTTP_400_BAD_REQUEST)

        config = ApprovalConfig.objects.filter(stage=eco.stage, user=request.user).first()
        if not config:
            return Response(
                {'error': 'You are not the designated approver for this stage.'},
                status=status.HTTP_403_FORBIDDEN
            )
        ApprovalRecord.objects.get_or_create(eco=eco, stage=eco.stage, user=request.user)
        log_event('approval_action', 'eco', eco.id, user=request.user,
                  new_value=f'Approved at {eco.stage.name}')

        # Auto-advance if all required approvals done
        required = ApprovalConfig.objects.filter(stage=eco.stage, category='required')
        if required.exists():
            all_done = all(
                ApprovalRecord.objects.filter(eco=eco, stage=eco.stage, user=c.user).exists()
                for c in required
            )
        else:
            # Bug 3 Fix: If there are no required approvers, do not let an optional approval auto-advance the stage.
            all_done = False

        if all_done:
            next_stage = get_next_stage(eco.stage)
            if next_stage:
                eco.stage = next_stage
                eco.save()
                log_event('stage_transition', 'eco', eco.id, user=request.user,
                          new_value=next_stage.name)
                if next_stage.is_default_done:
                    apply_eco(eco, request.user)
                    eco.refresh_from_db()

        return Response(ECODetailSerializer(eco).data)


class ECORejectView(APIView):
    permission_classes = [IsApproverOrAdmin]

    def post(self, request, pk):
        try:
            eco = ECO.objects.get(pk=pk)
        except ECO.DoesNotExist:
            return Response({'error': 'ECO not found'}, status=status.HTTP_404_NOT_FOUND)
        if eco.status != 'active':
            return Response({'error': 'Only active ECOs can be rejected.'}, status=status.HTTP_400_BAD_REQUEST)
        reason = request.data.get('reason', 'No reason provided')
        eco.status = 'rejected'
        eco.save()
        log_event('approval_action', 'eco', eco.id, user=request.user,
                  new_value=f'Rejected: {reason}')
        return Response({'message': 'ECO rejected.', 'reason': reason, 'status': eco.status})


class ECODiffView(APIView):
    """Returns all proposed changes for the ECO diff comparison view."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            eco = ECO.objects.get(pk=pk)
        except ECO.DoesNotExist:
            return Response({'error': 'ECO not found'}, status=status.HTTP_404_NOT_FOUND)
        changes = ECOProposedChange.objects.filter(eco=eco)
        data = [
            {
                'entity_type': c.entity_type,
                'field_name': c.field_name,
                'old_value': c.old_value,
                'new_value': c.new_value,
            }
            for c in changes
        ]
        return Response({'eco_id': pk, 'eco_type': eco.eco_type, 'changes': data})


class ECOProposedChangeCreateView(APIView):
    """Allows engineer to record a proposed change (from Open BOM / Open Product)."""
    permission_classes = [IsEngineeringOrAdmin]

    def post(self, request, pk):
        try:
            eco = ECO.objects.get(pk=pk)
        except ECO.DoesNotExist:
            return Response({'error': 'ECO not found'}, status=status.HTTP_404_NOT_FOUND)
        if eco.status != 'active':
            return Response({'error': 'Can only add changes to active ECOs.'},
                            status=status.HTTP_400_BAD_REQUEST)
        entity_type = request.data.get('entity_type')
        field_name  = request.data.get('field_name')
        old_value   = request.data.get('old_value')
        new_value   = request.data.get('new_value')
        if not all([entity_type, field_name, new_value]):
            return Response({'error': 'entity_type, field_name, new_value are required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Replace existing change for same field
        ECOProposedChange.objects.filter(eco=eco, entity_type=entity_type, field_name=field_name).delete()
        change = ECOProposedChange.objects.create(
            eco=eco, entity_type=entity_type,
            field_name=field_name, old_value=old_value, new_value=new_value
        )
        entity_id = eco.product_id if eco.eco_type == 'product' else eco.bom_id
        log_event('data_changed', eco.eco_type, entity_id, user=request.user,
                  field_name=field_name, old_value=old_value, new_value=new_value)
        return Response({'id': change.id, 'field_name': field_name,
                         'old_value': old_value, 'new_value': new_value},
                        status=status.HTTP_201_CREATED)
