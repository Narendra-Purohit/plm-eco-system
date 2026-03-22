from django.urls import path  # type: ignore
from .views import (ECOListCreateView, ECODetailView, ECOStartView,
                    ECOValidateView, ECOApproveView, ECORejectView,
                    ECODiffView, ECOProposedChangeCreateView)

urlpatterns = [
    path('ecos/', ECOListCreateView.as_view(), name='eco_list_create'),
    path('ecos/<int:pk>/', ECODetailView.as_view(), name='eco_detail'),
    path('ecos/<int:pk>/start/', ECOStartView.as_view(), name='eco_start'),
    path('ecos/<int:pk>/stage/next/', ECOValidateView.as_view(), name='eco_validate'),
    path('ecos/<int:pk>/approve/', ECOApproveView.as_view(), name='eco_approve'),
    path('ecos/<int:pk>/reject/', ECORejectView.as_view(), name='eco_reject'),
    path('ecos/<int:pk>/diff/', ECODiffView.as_view(), name='eco_diff'),
    path('ecos/<int:pk>/changes/', ECOProposedChangeCreateView.as_view(), name='eco_propose_change'),
]
