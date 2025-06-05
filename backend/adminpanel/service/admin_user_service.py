from devtools import debug

from accounts.models import CustomUser
from accounts.serializers.user_serializer import UserSerializer


class AdminUserService:
    def __init__(self):
        pass

    def get_all_users(self) -> UserSerializer:
        try:
            users = CustomUser.objects.all().order_by("-date_joined")
            serializer = UserSerializer(users, many=True)
        except CustomUser.DoesNotExist:
            debug("No users found in the database.")

        return serializer
