from rest_framework import serializers
from math import floor

from ..models import Product, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    """ "
    DRF Serializer for the Product model. Converts Product instances to JSON.
    """

    sale = serializers.SerializerMethodField()
    available = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    discount_percent = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_sale(self, obj):
        return obj.sale

    def get_available(self, obj):
        return obj.stock > 0

    def get_images(self, obj):
        all_images = []

        if obj.image:
            all_images.append({"image": obj.image.url})

        gallery = [{"image": img.image.url} for img in obj.images.all()]
        return all_images + gallery

    def get_discount_percent(self, obj):
        if obj.price_old and obj.price_old > obj.price_current:
            diff = obj.price_old - obj.price_current
            percent = (diff / obj.price_old) * 100
            return floor(percent)  # auf ganze Zahl abrunden
        return None


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]
