from django.db import models
from apps.users.models import CustomUser


class AuditLog(models.Model):
    """Immutable append-only audit trail for all critical PLM actions."""
    EVENT_TYPES = [
        ('eco_created', 'ECO Created'),
        ('stage_transition', 'Stage Transition'),
        ('approval_action', 'Approval Action'),
        ('version_created', 'Version Created'),
        ('data_changed', 'Data Changed'),
    ]

    event_type  = models.CharField(max_length=50, choices=EVENT_TYPES)
    entity_type = models.CharField(max_length=50)    # 'product', 'bom', 'eco'
    entity_id   = models.IntegerField()
    field_name  = models.CharField(max_length=100, null=True, blank=True)
    old_value   = models.TextField(null=True, blank=True)
    new_value   = models.TextField(null=True, blank=True)
    user        = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='audit_logs')
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp'], name='audit_event_time_idx'),
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            raise Exception("AuditLog entries are immutable and cannot be updated.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise Exception("AuditLog entries cannot be deleted.")

    def __str__(self):
        return f'[{self.timestamp}] {self.event_type} on {self.entity_type}#{self.entity_id} by {self.user.login_id}'
