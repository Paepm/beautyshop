from django.core.management.base import BaseCommand
from devtools.debug import debug

from accounts.models import CustomUser


class Command(BaseCommand):
    """Reactivates the admin user by setting is_deleted to False and is_active to True."""

    """--> call: python3 manage.py user_reactivate"""

    def handle(self, *args, **options):
        username = "admin"
        try:
            user = CustomUser.objects.get(username=username)
            user.is_deleted = False
            user.is_active = True
            user.set_password("testuser")
            user.save()
            debug(f"User '{username}' reactivated successfully.")
        except CustomUser.DoesNotExist:
            debug(f"User '{username}' does not exist.")
        except Exception as e:
            debug(f"An error occurred while reactivating user '{username}': {e}")
