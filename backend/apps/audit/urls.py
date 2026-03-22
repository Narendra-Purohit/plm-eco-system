from django.urls import path  # type: ignore
from .views import AuditLogView

urlpatterns = [
    path('audit/<str:entity_type>/<int:entity_id>/', AuditLogView.as_view(), name='audit_log'),
]
