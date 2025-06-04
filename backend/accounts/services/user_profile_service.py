from backend.accounts.serializers.user_serializer import UserSerializer


class UserProfileService:

    @staticmethod
    def get_user_profile(data) -> dict:
        """
        Returns the serialized user profile data.
        """
        data = UserSerializer(data)
        return data.data

    @staticmethod
    def update_user_profile(user, data):
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer, True
        return serializer, False
