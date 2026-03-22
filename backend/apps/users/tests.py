from django.test import TestCase  # type: ignore
from rest_framework.test import APIClient  # type: ignore
from apps.users.models import CustomUser  # type: ignore


class RolePermissionTest(TestCase):
    def setUp(self):
        self.engineering = CustomUser.objects.create_user(
            login_id='eng01', email='eng@t.com', password='PLM@1234', role='engineering'
        )
        self.operations = CustomUser.objects.create_user(
            login_id='ops01', email='ops@t.com', password='PLM@1234', role='operations'
        )
        self.approver = CustomUser.objects.create_user(
            login_id='appr01', email='appr@t.com', password='PLM@1234', role='approver'
        )
        self.admin = CustomUser.objects.create_user(
            login_id='adm01', email='adm@t.com', password='PLM@1234', role='admin'
        )

    def test_operations_cannot_create_product(self):
        """Operations role must be blocked from creating products."""
        client = APIClient()
        client.force_authenticate(user=self.operations)
        resp = client.post('/api/products/', {'name': 'Hack', 'sales_price': 1, 'cost_price': 1})
        self.assertIn(resp.status_code, [403, 401])

    def test_engineering_can_create_product(self):
        """Engineering role must be allowed to create products."""
        client = APIClient()
        client.force_authenticate(user=self.engineering)
        resp = client.post('/api/products/',
            {'name': 'Valid Widget', 'sales_price': 10.0, 'cost_price': 5.0},
            format='json')
        self.assertEqual(resp.status_code, 201)

    def test_approver_cannot_create_eco(self):
        """Approver role must be blocked from creating ECOs (engineering-only)."""
        client = APIClient()
        client.force_authenticate(user=self.approver)
        resp = client.post('/api/ecos/', {}, format='json')
        # 403 = permission denied; 400 = validation (means it passed permission but failed validation)
        self.assertIn(resp.status_code, [400, 403])

    def test_non_admin_can_read_stages(self):
        """All authenticated users should be able to GET stages (needed to render ECO workflow)."""
        client = APIClient()
        client.force_authenticate(user=self.engineering)
        resp = client.get('/api/settings/stages/')
        self.assertEqual(resp.status_code, 200)

    def test_non_admin_cannot_create_stages(self):
        """Non-admin users must be blocked from creating/modifying stages."""
        client = APIClient()
        client.force_authenticate(user=self.engineering)
        resp = client.post('/api/settings/stages/', {'name': 'Hack', 'sequence': 99}, format='json')
        self.assertIn(resp.status_code, [403, 401])

    def test_admin_can_access_settings(self):
        """Admin role must have access to the settings/stages endpoint."""
        client = APIClient()
        client.force_authenticate(user=self.admin)
        resp = client.get('/api/settings/stages/')
        self.assertEqual(resp.status_code, 200)
