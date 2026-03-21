from django.urls import path
from .views import (ECOStageListCreateView, ECOStageDetailView,
                    ApprovalConfigListCreateView, ApprovalConfigDetailView)

urlpatterns = [
    path('settings/stages/', ECOStageListCreateView.as_view(), name='stage_list_create'),
    path('settings/stages/<int:pk>/', ECOStageDetailView.as_view(), name='stage_detail'),
    path('settings/approvals/', ApprovalConfigListCreateView.as_view(), name='approval_list_create'),
    path('settings/approvals/<int:pk>/', ApprovalConfigDetailView.as_view(), name='approval_detail'),
]
