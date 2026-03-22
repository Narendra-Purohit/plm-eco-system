from django.core.management.base import BaseCommand  # type: ignore
from apps.users.models import CustomUser  # type: ignore
from apps.settings_app.models import ECOStage  # type: ignore
from apps.products.models import Product  # type: ignore
from apps.bom.models import BOM, BOMComponent, BOMOperation  # type: ignore


class Command(BaseCommand):
    help = 'Seed the PLM database with initial demo data'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding PLM database...')

        # ── ECO Stages ──────────────────────────────────────────────────────
        new_stage, created = ECOStage.objects.get_or_create(
            is_default_new=True,
            defaults={'name': 'New', 'sequence': 1}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Stage: New'))

        review_stage, created = ECOStage.objects.get_or_create(
            name='In Review',
            defaults={'sequence': 10, 'is_default_new': False, 'is_default_done': False}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Stage: In Review'))

        approval_stage, created = ECOStage.objects.get_or_create(
            name='Approval',
            defaults={'sequence': 20, 'is_default_new': False, 'is_default_done': False}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Stage: Approval'))

        done_stage, created = ECOStage.objects.get_or_create(
            is_default_done=True,
            defaults={'name': 'Done', 'sequence': 999}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Stage: Done'))

        # ── Users ────────────────────────────────────────────────────────────
        roles = [
            ('engineering01', 'engineering@plm.local', 'engineering'),
            ('approver01',    'approver@plm.local',    'approver'),
            ('operations01',  'operations@plm.local',  'operations'),
            ('admin01',       'admin@plm.local',       'admin'),
        ]
        for login_id, email, role in roles:
            if not CustomUser.objects.filter(login_id=login_id).exists():
                CustomUser.objects.create_user(
                    login_id=login_id, email=email,
                    password='PLM@1234', role=role
                )
                self.stdout.write(self.style.SUCCESS(f'  ✓ User: {login_id} / PLM@1234'))
            else:
                self.stdout.write(f'  → User {login_id} already exists')

        # ── Products ─────────────────────────────────────────────────────────
        p1, created = Product.objects.get_or_create(
            name='Widget A',
            defaults={'sales_price': 12.50, 'cost_price': 8.00, 'version': 1}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Product: Widget A'))

        p2, created = Product.objects.get_or_create(
            name='Component X',
            defaults={'sales_price': 3.00, 'cost_price': 1.50, 'version': 1}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Product: Component X'))

        p3, created = Product.objects.get_or_create(
            name='Assembly B',
            defaults={'sales_price': 45.00, 'cost_price': 30.00, 'version': 1}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Product: Assembly B'))

        # ── BOMs ─────────────────────────────────────────────────────────────
        if not BOM.objects.filter(product=p1).exists():
            bom = BOM.objects.create(product=p1, quantity=1, unit='Units')
            BOMComponent.objects.create(
                bom=bom, component_product=p2, quantity=3, unit='Units'
            )
            BOMOperation.objects.create(
                bom=bom, work_center='Assembly Line 1', expected_duration_mins=30
            )
            self.stdout.write(self.style.SUCCESS(f'  ✓ BOM: {bom.reference} for Widget A'))

        if not BOM.objects.filter(product=p3).exists():
            bom2 = BOM.objects.create(product=p3, quantity=1, unit='Units')
            BOMComponent.objects.create(
                bom=bom2, component_product=p1, quantity=2, unit='Units'
            )
            BOMComponent.objects.create(
                bom=bom2, component_product=p2, quantity=5, unit='Units'
            )
            BOMOperation.objects.create(
                bom=bom2, work_center='Assembly Line 2', expected_duration_mins=60
            )
            self.stdout.write(self.style.SUCCESS(f'  ✓ BOM: {bom2.reference} for Assembly B'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Database seeded successfully!'))
        self.stdout.write('\nTest credentials:')
        self.stdout.write('  engineering01 / PLM@1234 (role: engineering)')
        self.stdout.write('  approver01    / PLM@1234 (role: approver)')
        self.stdout.write('  operations01  / PLM@1234 (role: operations)')
        self.stdout.write('  admin01       / PLM@1234 (role: admin)')
