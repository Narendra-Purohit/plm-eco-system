from rest_framework import serializers  # type: ignore
from .models import Product, ProductAttachment


class ProductAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttachment
        fields = ['id', 'file_name', 'file_path', 'uploaded_at']


class ProductSerializer(serializers.ModelSerializer):
    attachments = ProductAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'sales_price', 'cost_price',
                  'version', 'status', 'created_at', 'updated_at', 'attachments']
        read_only_fields = ['id', 'version', 'status', 'created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    class Meta:
        model = Product
        fields = ['id', 'name', 'sales_price', 'cost_price', 'version', 'status', 'created_at']
