from django.core.management.base import BaseCommand
from shipping.services.dpd_scraper import DPDTrackingScraper


class Command(BaseCommand):
    help = "Mark orders as delivered based on DPD tracking results."

    def handle(self, *args, **kwargs):
        scraper = DPDTrackingScraper()
        result = scraper.run()

        self.stdout.write(self.style.SUCCESS("✅ DPD delivery check finished."))
        self.stdout.write(
            self.style.SUCCESS(f"📦 Delivered orders: {result['delivered']}")
        )
        self.stdout.write(
            self.style.WARNING(f"⏳ Still in transit: {result['in_transit']}")
        )
        self.stdout.write(self.style.NOTICE(f"❌ Failed: {result['failed']}"))
