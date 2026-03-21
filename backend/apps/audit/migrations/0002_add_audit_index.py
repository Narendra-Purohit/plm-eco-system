from django.db import migrations, models


class Migration(migrations.Migration):
    """Adds performance index for the AuditLog model."""

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['event_type', 'timestamp'], name='audit_event_time_idx'),
        ),
    ]
