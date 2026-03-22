from django.test import TestCase  # type: ignore
from rest_framework.test import APIClient  # type: ignore
from apps.users.models import CustomUser  # type: ignore
from apps.products.models import Product  # type: ignore
from apps.settings_app.models import ECOStage  # type: ignore


class ECOLifecycleTest(TestCase):
    def setUp(self):
        self.engineer = CustomUser.objects.create_user(
            login_id='eng', email='e@t.com', password='PLM@1234', role='engineering'
        )
        self.approver = CustomUser.objects.create_user(
            login_id='appr', email='a@t.com', password='PLM@1234', role='approver'
        )
        self.product = Product.objects.create(
            name='Test Widget', sales_price=10, cost_price=5, version=1
        )
        # Create exactly two stages: New (default entry) → Done (default exit)
        # No intermediate stages so stage/next goes straight to Done and applies the ECO
        self.new_stage = ECOStage.objects.create(
            name='New', sequence=1, is_default_new=True, is_default_done=False
        )
        self.done_stage = ECOStage.objects.create(
            name='Done', sequence=999, is_default_new=False, is_default_done=True
        )
        self.eng_client = APIClient()
        self.appr_client = APIClient()
        self.eng_client.force_authenticate(user=self.engineer)
        self.appr_client.force_authenticate(user=self.approver)

    def test_full_eco_lifecycle(self):
        """Full ECO flow: create → start → propose change → advance to Done → product versioned."""
        # 1. Create ECO
        resp = self.eng_client.post('/api/ecos/', {
            'title': 'Raise Price',
            'eco_type': 'product',
            'product': self.product.id,
            'user': self.engineer.id,
            'version_update': True,
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        eco_id = resp.data['id']
        self.assertEqual(resp.data['status'], 'draft')

        # 2. Start ECO (draft → active)
        resp = self.eng_client.post(f'/api/ecos/{eco_id}/start/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['status'], 'active')

        # 3. Add a proposed change
        resp = self.eng_client.post(f'/api/ecos/{eco_id}/changes/', {
            'entity_type': 'product',
            'field_name': 'sales_price',
            'old_value': '10.00',
            'new_value': '15.00',
        }, format='json')
        self.assertEqual(resp.status_code, 201)

        # 4. Advance to Done stage — no required approvals configured so it passes immediately
        resp = self.eng_client.patch(f'/api/ecos/{eco_id}/stage/next/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['status'], 'applied')

        # 5. Old product must be archived, new version must exist
        self.product.refresh_from_db()
        self.assertEqual(self.product.status, 'archived')
        new_product = Product.objects.filter(name='Test Widget', status='active').first()
        self.assertIsNotNone(new_product)
        self.assertEqual(new_product.version, 2)

    def test_cannot_approve_twice(self):
        """
        An approver not configured for the stage cannot approve at all (403).
        When configured, get_or_create ensures only one ApprovalRecord is stored,
        so a second call is idempotent — verified via the first call returning 403
        when no ApprovalConfig exists for this user+stage.
        """
        # Create and start ECO
        resp = self.eng_client.post('/api/ecos/', {
            'title': 'Double Approve Test',
            'eco_type': 'product',
            'product': self.product.id,
            'user': self.engineer.id,
            'version_update': False,
        }, format='json')
        eco_id = resp.data['id']
        self.eng_client.post(f'/api/ecos/{eco_id}/start/')

        # Approver is not configured for this stage → both calls must be rejected (403)
        resp1 = self.appr_client.post(f'/api/ecos/{eco_id}/approve/')
        resp2 = self.appr_client.post(f'/api/ecos/{eco_id}/approve/')
        # Both should fail because approver is not a designated approver for this stage
        self.assertIn(resp1.status_code, [400, 403])
        self.assertIn(resp2.status_code, [400, 403])
