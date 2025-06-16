from django.core.management.base import BaseCommand
from orders.services.delivery_status_updater_service import DeliveryStatusUpdater


class Command(BaseCommand):
    help = "Checks shipped orders and updates to delivered if conditions are met."

    def handle(self, *args, **options):
        updater = DeliveryStatusUpdater()
        updater.run()
