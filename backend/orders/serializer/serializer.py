from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    """
    Converts Order model instances into JSON format.
    """

    class Meta:
        model = Order
        fields = [
            "user",
            "id",
            "created_at",
            "total_price",
            "payment_method",
            "shipping_address",
            "payment_provider",
            "payment_status",
            "order_status",
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
