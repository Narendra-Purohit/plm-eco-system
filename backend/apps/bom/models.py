from django.core.exceptions import ValidationError
from django.db import models
from apps.products.models import Product


class BOM(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('archived', 'Archived')]

    reference  = models.CharField(max_length=20, blank=True)
    product    = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='boms')
    quantity   = models.DecimalField(max_digits=10, decimal_places=3, default=1)
    unit       = models.CharField(max_length=50, default='Units')
    version    = models.IntegerField(default=1)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('reference', 'version')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        reference_needs_generation = not self.reference

        if not is_new:
            try:
                old = BOM.objects.get(pk=self.pk)
                if old.status == 'archived':
                    raise ValidationError("Archived BOMs cannot be modified.")
            except BOM.DoesNotExist:
                pass

        if reference_needs_generation:
            # Save first to acquire a mathematically guaranteed unique Database ID
            super().save(*args, **kwargs)
            self.reference = f'BOM-{str(self.id).zfill(4)}'
            # Update only the reference field
            kwargs.pop('force_insert', None)
            kwargs['force_update'] = True
            super().save(update_fields=['reference'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.reference} - {self.product.name} (v{self.version})'


class BOMComponent(models.Model):
    bom               = models.ForeignKey(BOM, on_delete=models.CASCADE, related_name='components')
    component_product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity          = models.DecimalField(max_digits=10, decimal_places=3)
    unit              = models.CharField(max_length=50, default='Units')

    def clean(self):
        if hasattr(self, 'bom') and hasattr(self, 'component_product'):
            # Bug 4 Fix: Prevent Circular Dependencies
            if self.bom.product_id == self.component_product_id:
                raise ValidationError("A BOM cannot contain its own product as a component.")
            
            # Bug 4 Fix: Prevent rigidly linking historical/archived products into active structures
            if getattr(self.bom, 'status', None) == 'active' and getattr(self.component_product, 'status', None) == 'archived':
                raise ValidationError("An active BOM cannot use an archived product as a component.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.component_product.name} x{self.quantity} in {self.bom.reference}'


class BOMOperation(models.Model):
    bom                    = models.ForeignKey(BOM, on_delete=models.CASCADE, related_name='operations')
    work_center            = models.CharField(max_length=255)
    expected_duration_mins = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.work_center} ({self.expected_duration_mins} min) in {self.bom.reference}'
