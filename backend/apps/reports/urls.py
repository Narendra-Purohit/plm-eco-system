from django.urls import path
from .views import (ECOReportView, ProductVersionHistoryReportView,
                    BOMHistoryReportView, ArchivedReportView)

urlpatterns = [
    path('reports/ecos/', ECOReportView.as_view(), name='report_ecos'),
    path('reports/product-versions/', ProductVersionHistoryReportView.as_view(), name='report_product_versions'),
    path('reports/bom-history/', BOMHistoryReportView.as_view(), name='report_bom_history'),
    path('reports/archived/', ArchivedReportView.as_view(), name='report_archived'),
]
