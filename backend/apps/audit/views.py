from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdminOnly
from .models import AuditLog


class AuditLogView(APIView):
    """Returns audit logs for a specific entity. Admin only."""
    permission_classes = [IsAdminOnly]

    def get(self, request, entity_type, entity_id):
        logs = AuditLog.objects.filter(
            entity_type=entity_type, entity_id=entity_id
        ).order_by('-timestamp')
        data = [
            {
                'id': log.id,
                'event_type': log.event_type,
                'entity_type': log.entity_type,
                'entity_id': log.entity_id,
                'field_name': log.field_name,
                'old_value': log.old_value,
                'new_value': log.new_value,
                'user': log.user.login_id,
                'timestamp': log.timestamp,
            }
            for log in logs
        ]
        return Response(data)
