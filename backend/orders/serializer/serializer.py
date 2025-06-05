from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    """
    Converts Order model instances into JSON format.
    """

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "payment_status",
            "payment_provider",
            "payment_method",
            "total_price",
            "created_at",
            "updated_at",
            "items",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Converts Order model instances into JSON format.
    """

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)
    product_description = serializers.CharField(
        source="product.description", read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "product_name",
            "product_image",
            "product_description",
            "quantity",
            "price",
        ]
