from django.core.exceptions import ValidationError  # type: ignore
from django.db import models  # type: ignore


class Product(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('archived', 'Archived')]

    name        = models.CharField(max_length=255)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_price  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    version     = models.IntegerField(default=1)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old = Product.objects.get(pk=self.pk)
                if old.status == 'archived' and self.status == 'archived':
                    raise ValidationError("Archived products cannot be modified.")
            except Product.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} (v{self.version}) [{self.status}]'


class ProductAttachment(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attachments')
    file_name   = models.CharField(max_length=255)
    file_path   = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file_name} → {self.product.name}'
