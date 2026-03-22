from django.db import models  # type: ignore
from apps.users.models import CustomUser  # type: ignore
from apps.products.models import Product  # type: ignore
from apps.bom.models import BOM  # type: ignore
from apps.settings_app.models import ECOStage  # type: ignore


class ECO(models.Model):
    ECO_TYPE_CHOICES = [('product', 'Product'), ('bom', 'Bill of Materials')]
    STATUS_CHOICES   = [('draft', 'Draft'), ('active', 'Active'), ('applied', 'Applied'), ('rejected', 'Rejected')]

    title          = models.CharField(max_length=255)
    eco_type       = models.CharField(max_length=20, choices=ECO_TYPE_CHOICES)
    product        = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='ecos')
    bom            = models.ForeignKey(BOM, on_delete=models.PROTECT, null=True, blank=True, related_name='ecos')
    user           = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='ecos')
    effective_date = models.DateTimeField(null=True, blank=True)
    version_update = models.BooleanField(default=True)
    stage          = models.ForeignKey(ECOStage, on_delete=models.PROTECT)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status'], name='eco_status_idx'),
            models.Index(fields=['product', 'status'], name='eco_product_status_idx'),
        ]
        
    def __str__(self):
        return f'ECO: {self.title} [{self.status}]'


class ECOProposedChange(models.Model):
    ENTITY_TYPE_CHOICES = [
        ('product', 'Product'), 
        ('bom', 'BOM'), 
        ('bomcomponent', 'BOM Component')
    ]

    eco         = models.ForeignKey(ECO, on_delete=models.CASCADE, related_name='proposed_changes')
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    field_name  = models.CharField(max_length=100)
    old_value   = models.TextField(null=True, blank=True)
    new_value   = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.eco.title} | {self.field_name}: {self.old_value} → {self.new_value}'
