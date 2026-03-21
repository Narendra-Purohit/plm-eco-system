from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.eco.models import ECO
from apps.products.models import Product
from apps.bom.models import BOM


class ECOReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ecos = ECO.objects.select_related('product', 'stage', 'user').order_by('-created_at')
        data = [
            {
                'id': e.id,
                'title': e.title,
                'eco_type': e.eco_type,
                'product_name': e.product.name,
                'stage': e.stage.name,
                'status': e.status,
                'effective_date': e.effective_date,
                'created_at': e.created_at,
            }
            for e in ecos
        ]
        return Response(data)


class ProductVersionHistoryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all().order_by('name', 'version')
        data = [
            {
                'id': p.id,
                'name': p.name,
                'version': p.version,
                'status': p.status,
                'sales_price': str(p.sales_price),
                'cost_price': str(p.cost_price),
                'created_at': p.created_at,
            }
            for p in products
        ]
        return Response(data)


class BOMHistoryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boms = BOM.objects.select_related('product').order_by('product__name', 'version')
        data = [
            {
                'id': b.id,
                'reference': b.reference,
                'product_name': b.product.name,
                'version': b.version,
                'status': b.status,
                'created_at': b.created_at,
            }
            for b in boms
        ]
        return Response(data)


class ArchivedReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        archived_products = Product.objects.filter(status='archived').order_by('name', 'version')
        archived_boms = BOM.objects.filter(status='archived').order_by('product__name', 'version')
        return Response({
            'archived_products': [
                {'id': p.id, 'name': p.name, 'version': p.version, 'created_at': p.created_at}
                for p in archived_products
            ],
            'archived_boms': [
                {'id': b.id, 'reference': b.reference, 'product': b.product.name,
                 'version': b.version, 'created_at': b.created_at}
                for b in archived_boms
            ],
        })
