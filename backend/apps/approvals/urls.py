from django.urls import path  # type: ignore
from .views import ApprovalConfigListView, ApprovalConfigCreateView

urlpatterns = [
    path('approvals/', ApprovalConfigListView.as_view(), name='approval_list'),
    path('approvals/create/', ApprovalConfigCreateView.as_view(), name='approval_create'),
]
