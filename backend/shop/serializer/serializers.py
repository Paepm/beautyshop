from rest_framework import serializers
from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    """ "
    DRF Serializer for the Product model. Converts Product instances to JSON.
    """

    sale = serializers.SerializerMethodField()
    available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_sale(self, obj):
        return obj.sale

    def get_available(self, obj):
        return obj.stock > 0
