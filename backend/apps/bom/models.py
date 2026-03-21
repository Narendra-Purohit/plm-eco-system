from django.core.exceptions import ValidationError
from django.db import models
from apps.products.models import Product


class BOM(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('archived', 'Archived')]

    reference  = models.CharField(max_length=8, unique=True, blank=True)
    product    = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='boms')
    quantity   = models.DecimalField(max_digits=10, decimal_places=3, default=1)
    unit       = models.CharField(max_length=50, default='Units')
    version    = models.IntegerField(default=1)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            count = BOM.objects.count()
            self.reference = f'BOM-{str(count + 1).zfill(4)}'
        if self.pk:
            try:
                old = BOM.objects.get(pk=self.pk)
                if old.status == 'archived':
                    raise ValidationError("Archived BOMs cannot be modified.")
            except BOM.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.reference} - {self.product.name} (v{self.version})'


class BOMComponent(models.Model):
    bom               = models.ForeignKey(BOM, on_delete=models.CASCADE, related_name='components')
    component_product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity          = models.DecimalField(max_digits=10, decimal_places=3)
    unit              = models.CharField(max_length=50, default='Units')

    def __str__(self):
        return f'{self.component_product.name} x{self.quantity} in {self.bom.reference}'


class BOMOperation(models.Model):
    bom                    = models.ForeignKey(BOM, on_delete=models.CASCADE, related_name='operations')
    work_center            = models.CharField(max_length=255)
    expected_duration_mins = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.work_center} ({self.expected_duration_mins} min) in {self.bom.reference}'
