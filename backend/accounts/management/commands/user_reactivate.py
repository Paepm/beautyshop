from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        username = "admin"

        user = CustomUser.objects.get(username=username)
        user.is_deleted = False
        user.is_active = True
        user.password = "testuser"
        user.save()
