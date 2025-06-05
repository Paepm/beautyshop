# payments/services/checkout_service.py

from orders.services.order_creator_service import OrderCreatorService
from payments.services.payment_dispatcher import PaymentDispatcher
from devtools import debug
from orders.models import Order


class CheckoutService:
    def __init__(self, user):
        self.user = user
        self.order: Order | None = None

    def create_order(
        self, payment_provider, shipping_data, payment_method
    ) -> Order | None:
        """
        Create an order for the current user using the selected payment provider.
        """
        creator = OrderCreatorService(self.user)
        self.order = creator.create_order(
            payment_provider=payment_provider,
            shipping_data=shipping_data,
            payment_method=payment_method,
        )
        return self.order

    def save_shipping_info(self, shipping_data: dict, payment_method: str) -> None:
        """
        Save shipping address and selected payment method to the order.
        """
        if not self.order:
            raise ValueError("Order not initialized.")

        self.order.shipping_address = (
            f"{shipping_data.get('address', '')}, "
            f"{shipping_data.get('post_code', '')} "
            f"{shipping_data.get('city', '')}, "
            f"{shipping_data.get('country', '')}"
        )
        self.order.payment_method = payment_method
        self.order.save(update_fields=["shipping_address", "payment_method"])

    def start_checkout(self, success_url: str, cancel_url: str) -> str:
        """
        Dispatch the payment provider checkout session and return redirect URL.
        """
        if not self.order:
            raise ValueError("Order not initialized.")

        dispatcher = PaymentDispatcher(
            order=self.order, payment_method=self.order.payment_method
        )
        return dispatcher.dispatch(success_url, cancel_url)
