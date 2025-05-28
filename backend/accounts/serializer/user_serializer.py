from rest_framework import serializers

from accounts.models import CustomUser
from django_countries.fields import CountryField
from django_countries.serializer_fields import CountryField as CountrySerializerField


class UserSerializer(serializers.ModelSerializer):
    # country is not a field in CustomUser, but a CountryField
    country = CountrySerializerField()

    class Meta:
        model = CustomUser
        exclude = [
            "password",
            "is_superuser",
            "user_permissions",
            "groups",
        ]  # sensible fields enabled
        read_only_fields = [
            "id",
            "last_login",
            "is_staff",
            "is_active",
            "date_joined",
        ]
