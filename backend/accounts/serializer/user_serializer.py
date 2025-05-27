from rest_framework import serializers

from accounts.models import CustomUser  # the custom user model


class UserSerializer(serializers.ModelSerializer):
    # country is not a JSON so need to use source seperatly
    country = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = CustomUser
        exclude = [
            "password",
            "is_superuser",
            "user_permissions",
        ]  # sensible fields enabled
        read_only_fields = [
            "id",
            "last_login",
            "is_staff",
            "is_active",
            "date_joined",
        ]
