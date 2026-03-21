from rest_framework import serializers
from .models import BOM, BOMComponent, BOMOperation
from apps.products.models import Product


class BOMComponentSerializer(serializers.ModelSerializer):
    component_product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(status='active'),
        source='component_product'
    )
    component_product_name = serializers.CharField(source='component_product.name', read_only=True)

    class Meta:
        model = BOMComponent
        fields = ['id', 'component_product_id', 'component_product_name', 'quantity', 'unit']


class BOMOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMOperation
        fields = ['id', 'work_center', 'expected_duration_mins']


class BOMSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(status='active'),
        source='product'
    )
    product_name = serializers.CharField(source='product.name', read_only=True)
    components   = BOMComponentSerializer(many=True, required=False)
    operations   = BOMOperationSerializer(many=True, required=False)

    class Meta:
        model = BOM
        fields = ['id', 'reference', 'product_id', 'product_name',
                  'quantity', 'unit', 'version', 'status',
                  'created_at', 'updated_at', 'components', 'operations']
        read_only_fields = ['id', 'reference', 'version', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        components_data = validated_data.pop('components', [])
        operations_data = validated_data.pop('operations', [])
        bom = BOM.objects.create(**validated_data)
        for c in components_data:
            BOMComponent.objects.create(bom=bom, **c)
        for o in operations_data:
            BOMOperation.objects.create(bom=bom, **o)
        return bom


class BOMListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = BOM
        fields = ['id', 'reference', 'product_id', 'product_name', 'version', 'status', 'created_at']
