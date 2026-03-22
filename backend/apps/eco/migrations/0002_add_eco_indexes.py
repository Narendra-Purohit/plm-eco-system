from django.db import migrations, models  # type: ignore


class Migration(migrations.Migration):
    """Adds performance indexes for the ECO model."""

    dependencies = [
        ('eco', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='eco',
            index=models.Index(fields=['status'], name='eco_status_idx'),
        ),
        migrations.AddIndex(
            model_name='eco',
            index=models.Index(fields=['product', 'status'], name='eco_product_status_idx'),
        ),
    ]
