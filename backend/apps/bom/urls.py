from django.urls import path  # type: ignore
from .views import BOMListCreateView, BOMDetailView

urlpatterns = [
    path('boms/', BOMListCreateView.as_view(), name='bom_list_create'),
    path('boms/<int:pk>/', BOMDetailView.as_view(), name='bom_detail'),
]
