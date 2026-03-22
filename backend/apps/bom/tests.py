from django.test import TestCase  # type: ignore
from apps.bom.models import BOM  # type: ignore
from apps.products.models import Product  # type: ignore


class BOMTest(TestCase):
    def test_bom_auto_reference(self):
        """BOM reference must be auto-generated on save in BOM-XXXX format."""
        product = Product.objects.create(
            name='Widget', sales_price=10, cost_price=5, version=1
        )
        bom = BOM.objects.create(product=product, quantity=1, unit='Units')
        self.assertTrue(bom.reference.startswith('BOM'))
        self.assertGreater(len(bom.reference), 3)

    def test_bom_reference_is_unique(self):
        """Each BOM must get a distinct auto-generated reference."""
        product = Product.objects.create(
            name='Gadget', sales_price=20, cost_price=10, version=1
        )
        bom1 = BOM.objects.create(product=product, quantity=1, unit='Units')
        bom2 = BOM.objects.create(product=product, quantity=2, unit='Units')
        self.assertNotEqual(bom1.reference, bom2.reference)
