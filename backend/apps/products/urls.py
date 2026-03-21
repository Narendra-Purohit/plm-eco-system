from django.urls import path
from .views import ProductListCreateView, ProductDetailView, ProductVersionHistoryView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/versions/', ProductVersionHistoryView.as_view(), name='product_versions'),
]
