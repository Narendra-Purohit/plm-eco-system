from django.db import models  # type: ignore
from apps.users.models import CustomUser  # type: ignore
from apps.settings_app.models import ECOStage  # type: ignore


class ApprovalConfig(models.Model):
    CATEGORY_CHOICES = [('required', 'Required'), ('optional', 'Optional')]

    stage    = models.ForeignKey(ECOStage, on_delete=models.PROTECT, related_name='approvals')
    user     = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='approval_configs')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    class Meta:
        unique_together = ['stage', 'user']

    def __str__(self):
        return f'{self.stage.name} → {self.user.login_id} ({self.category})'


class ApprovalRecord(models.Model):
    """Tracks individual approval actions on an ECO."""

    eco         = models.ForeignKey('eco.ECO', on_delete=models.CASCADE, related_name='approval_records')
    stage       = models.ForeignKey(ECOStage, on_delete=models.CASCADE)
    user        = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['eco', 'stage', 'user']

    def __str__(self):
        return f'{self.user.login_id} approved ECO#{self.eco.id} at {self.stage.name}'
