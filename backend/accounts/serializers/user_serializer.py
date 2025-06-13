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
            "user_permissions",
            "groups",
        ]  # sensible fields enabled

        read_only_fields = [
            "id",
            "last_login",
            "is_active",
            "date_joined",
            "is_superuser",
        ]

    def validate_country(self, value):
        allowed_countries = ["AT", "DE", "LI", "CH"]
        if value.code not in allowed_countries:
            raise serializers.ValidationError("Only AT, DE, LI, and CH are allowed.")
        return value
