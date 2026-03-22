from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from .models import BOM, BOMComponent, BOMOperation
from .serializers import BOMSerializer, BOMListSerializer
from apps.users.permissions import IsEngineeringOrAdmin  # type: ignore
from apps.audit.utils import log_event  # type: ignore


class BOMListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsEngineeringOrAdmin()]
        return [IsAuthenticated()]

    def get(self, request):
        qs = BOM.objects.all().order_by('-created_at')
        search = request.query_params.get('search', '')
        if search:
            qs = qs.filter(product__name__icontains=search)
        status_filter = request.query_params.get('status', '')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return Response(BOMListSerializer(qs, many=True).data)

    def post(self, request):
        serializer = BOMSerializer(data=request.data)
        if serializer.is_valid():
            bom = serializer.save()
            log_event('data_changed', 'bom', bom.id, user=request.user, new_value=bom.reference)
            return Response(BOMSerializer(bom).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BOMDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsEngineeringOrAdmin()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        try:
            bom = BOM.objects.get(pk=pk)
        except BOM.DoesNotExist:
            return Response({'error': 'BOM not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BOMSerializer(bom).data)

    def patch(self, request, pk):
        try:
            bom = BOM.objects.get(pk=pk)
        except BOM.DoesNotExist:
            return Response({'error': 'BOM not found'}, status=status.HTTP_404_NOT_FOUND)
        if bom.status == 'archived':
            return Response({'error': 'Archived BOMs cannot be modified.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BOMSerializer(bom, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            bom.refresh_from_db()
            log_event('data_changed', 'bom', bom.id, user=request.user, new_value='updated')
            return Response(BOMSerializer(bom).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
