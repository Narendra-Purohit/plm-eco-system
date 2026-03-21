import os
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.conf import settings as django_settings
from .models import Product, ProductAttachment
from .serializers import ProductSerializer, ProductListSerializer
from apps.users.permissions import IsEngineeringOrAdmin


class ProductListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsEngineeringOrAdmin()]
        return [IsAuthenticated()]

    def get(self, request):
        qs = Product.objects.all().order_by('-created_at')
        search = request.query_params.get('search', '')
        if search:
            qs = qs.filter(name__icontains=search)
        status_filter = request.query_params.get('status', '')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return Response(ProductListSerializer(qs, many=True).data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product = serializer.save()
        # Handle file attachments
        files = request.FILES.getlist('attachments')
        for f in files:
            upload_dir = os.path.join(django_settings.MEDIA_ROOT, 'products', str(product.id))
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, f.name)
            with open(file_path, 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)
            rel_path = f'/media/products/{product.id}/{f.name}'
            ProductAttachment.objects.create(product=product, file_name=f.name, file_path=rel_path)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product).data)


class ProductVersionHistoryView(APIView):
    """Returns all versions of products with the same name."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        versions = Product.objects.filter(name=product.name).order_by('version')
        return Response(ProductListSerializer(versions, many=True).data)
