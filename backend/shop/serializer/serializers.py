from rest_framework import serializers
from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    """ "
    DRF Serializer for the Product model. Converts Product instances to JSON.
    """

    class Meta:
        model = Product
        fields = "__all__"
