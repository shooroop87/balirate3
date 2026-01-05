from django.core.management.base import BaseCommand
from subscriptions.models import Plan


class Command(BaseCommand):
    help = 'Создание тарифных планов BlisterPerPost'

    def handle(self, *args, **options):
        plans_data = [
            {
                'name': 'Wöchentlich',
                'slug': 'woechentlich',
                'description': 'Ideal zum Testen oder für kurzfristige Therapien',
                'interval_days': '7',
                'price': 8.90,
                'is_active': True,
                'is_featured': False,
                'trial_days': 0,
                'features': [
                    'Apothekengeprüfte Blisterkarte für 7 Tage',
                    'Klar getrennte Tageszeiten',
                    'Pharmazeutische Prüfung auf Wechselwirkungen',
                    'Versand per DHL',
                ],
            },
            {
                'name': 'Monatlich',
                'slug': 'monatlich',
                'description': 'Unser beliebtester Service – sicher, einfach und automatisch',
                'interval_days': '28',
                'price': 34.90,
                'is_active': True,
                'is_featured': True,
                'trial_days': 28,  # Erster Monat gratis
                'features': [
                    '4 wöchentliche Blisterkarten pro Monat',
                    'Pharmazeutische Kontrolle und Verträglichkeitsprüfung',
                    'Erster Monat kostenlos inkl. Lieferung',
                    'Automatische Lieferung',
                ],
            },
            {
                'name': 'Vierteljährlich',
                'slug': 'vierteljaehrlich',
                'description': 'Optimal für Langzeittherapien und Pflegeeinrichtungen',
                'interval_days': '28',  # Используем 28 как базу
                'price': 99.00,
                'is_active': True,
                'is_featured': False,
                'trial_days': 28,
                'features': [
                    '12 Blisterkarten sorgfältig vorbereitet',
                    'Direkte Abstimmung mit Ärzt:innen',
                    'Kostenloser Austausch bei Therapieänderungen',
                    'Ideal für Pflegeeinrichtungen',
                ],
            },
        ]

        for plan_data in plans_data:
            plan, created = Plan.objects.update_or_create(
                slug=plan_data['slug'],
                defaults=plan_data
            )
            status = 'Erstellt' if created else 'Aktualisiert'
            self.stdout.write(
                self.style.SUCCESS(f'{status}: {plan.name} - {plan.price}€')
            )

        self.stdout.write(self.style.SUCCESS('\nAlle Pläne erfolgreich erstellt!'))