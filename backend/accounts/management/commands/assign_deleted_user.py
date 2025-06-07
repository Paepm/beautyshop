from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from orders.models import Order


class Command(BaseCommand):
    help = "Assigns a deleted user to all orphaned orders"

    def handle(self, *args, **options):
        deleted_user = CustomUser.objects.get(username="deleted_user")
        orders = Order.objects.filter(user__isnull=True)
        for order in orders:
            order.user = deleted_user
            order.save()
        self.stdout.write(self.style.SUCCESS("Done."))
