from rest_framework import serializers
from orders.models import Order, OrderItem
from shop.models import Product
from accounts.models import CustomUser


class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "slug",
            "on_sale",
            "description",
            "price",
            "old_price",
            "available",
            "image",
            "created",
            "updated",
        ]


class AdminOrderItemSerializer(serializers.ModelSerializer):
    product = AdminProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "gender",
            "is_active",
            "is_staff",
            "is_superuser",
            "email",
            "username",
            "country",
            "city",
            "address",
            "post_code",
            "phone_number",
            "date_of_birth",
            "newsletter_opt_in",
            "terms_accepted",
        ]


class AdminOrderSerializer(serializers.ModelSerializer):
    items = AdminOrderItemSerializer(source="orderitem_set", many=True, read_only=True)
    user = AdminUserSerializer(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "username",
            "user",
            "created_at",
            "shipping_address",
            "shipping_method",
            "shipping_cost",
            "shipping_city",
            "shipping_post_code",
            "shipping_country",
            "order_status",
            "payment_status",
            "payment_provider",
            "payment_method",
            "total_price",
            "items",
        ]
