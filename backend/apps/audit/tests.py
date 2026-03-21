from django.test import TestCase
from apps.audit.models import AuditLog
from apps.users.models import CustomUser


class AuditLogImmutabilityTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            login_id='auditor', email='audit@test.com',
            password='PLM@1234', role='engineering'
        )
        self.user2 = CustomUser.objects.create_user(
            login_id='auditor2', email='audit2@test.com',
            password='PLM@1234', role='engineering'
        )

    def test_audit_log_cannot_be_updated(self):
        """AuditLog records must never be editable."""
        log = AuditLog.objects.create(
            event_type='eco_created',
            entity_type='eco',
            entity_id=1,
            user=self.user,
        )
        original_event = log.event_type
        with self.assertRaises(Exception):
            log.event_type = 'stage_transition'
            log.save()  # Should raise — AuditLog.save() blocks updates
        log.refresh_from_db()
        self.assertEqual(log.event_type, original_event)

    def test_audit_log_cannot_be_deleted(self):
        """AuditLog records must never be deletable."""
        log = AuditLog.objects.create(
            event_type='eco_created',
            entity_type='eco',
            entity_id=2,
            user=self.user2,
        )
        with self.assertRaises(Exception):
            log.delete()  # Should raise — AuditLog.delete() is blocked
        # Confirm it still exists in DB
        self.assertTrue(AuditLog.objects.filter(pk=log.pk).exists())
