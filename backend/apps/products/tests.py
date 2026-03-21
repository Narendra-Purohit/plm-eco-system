from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import CustomUser
from apps.products.models import Product


class ProductIntegrityTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            login_id='testeng', email='eng@test.com',
            password='PLM@1234', role='engineering'
        )
        self.client.force_authenticate(user=self.user)

    def test_cannot_edit_archived_product_at_model_level(self):
        """Archived products must be read-only at the model layer."""
        product = Product.objects.create(
            name='Old Widget', sales_price=10, cost_price=5,
            version=1, status='archived'
        )
        with self.assertRaises((ValidationError, Exception)):
            product.sales_price = 99
            product.save()

    def test_cannot_edit_archived_product_via_api(self):
        """Archived products must be read-only via the API (no PATCH endpoint)."""
        product = Product.objects.create(
            name='Old Widget API', sales_price=10, cost_price=5,
            version=1, status='archived'
        )
        # ProductDetailView only has GET — PATCH returns 405 Method Not Allowed
        resp = self.client.patch(f'/api/products/{product.id}/', {'sales_price': 99})
        self.assertIn(resp.status_code, [400, 403, 405])
