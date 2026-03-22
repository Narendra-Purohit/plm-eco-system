from rest_framework import serializers  # type: ignore
from .models import ECO, ECOProposedChange
from apps.settings_app.models import ECOStage  # type: ignore
from apps.products.serializers import ProductListSerializer  # type: ignore
from apps.bom.serializers import BOMListSerializer  # type: ignore


class ECOProposedChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECOProposedChange
        fields = ['id', 'entity_type', 'field_name', 'old_value', 'new_value']


class ECOSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views and create."""
    product_name = serializers.CharField(source='product.name', read_only=True)
    stage_name   = serializers.CharField(source='stage.name', read_only=True)
    user_name    = serializers.CharField(source='user.login_id', read_only=True)
    bom_reference = serializers.CharField(source='bom.reference', read_only=True, allow_null=True)

    class Meta:
        model = ECO
        fields = ['id', 'title', 'eco_type', 'product', 'product_name',
                  'bom', 'bom_reference', 'user', 'user_name',
                  'effective_date', 'version_update', 'stage', 'stage_name',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'effective_date', 'stage', 'status', 'created_at', 'updated_at']


class ECODetailSerializer(serializers.ModelSerializer):
    """Full serializer with proposed changes and stage info."""
    product_name    = serializers.CharField(source='product.name', read_only=True)
    stage_name      = serializers.CharField(source='stage.name', read_only=True)
    stage_sequence  = serializers.IntegerField(source='stage.sequence', read_only=True)
    is_done         = serializers.BooleanField(source='stage.is_default_done', read_only=True)
    user_name       = serializers.CharField(source='user.login_id', read_only=True)
    bom_reference   = serializers.CharField(source='bom.reference', read_only=True, allow_null=True)
    proposed_changes = ECOProposedChangeSerializer(many=True, read_only=True)

    class Meta:
        model = ECO
        fields = ['id', 'title', 'eco_type', 'product', 'product_name',
                  'bom', 'bom_reference', 'user', 'user_name',
                  'effective_date', 'version_update',
                  'stage', 'stage_name', 'stage_sequence', 'is_done',
                  'status', 'created_at', 'updated_at', 'proposed_changes']
