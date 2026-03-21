from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import BOM
from .serializers import BOMSerializer, BOMListSerializer
from apps.users.permissions import IsEngineeringOrAdmin


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
            return Response(BOMSerializer(bom).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BOMDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            bom = BOM.objects.get(pk=pk)
        except BOM.DoesNotExist:
            return Response({'error': 'BOM not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BOMSerializer(bom).data)
