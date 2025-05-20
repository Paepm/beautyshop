from orders.models import Order
from payments.services.provider_registry import PROVIDER_MAP
from payments.enums.payment_methods import PaymentMethod


class PaymentService:
    """Handles payment methods and processes payments for orders."""

    def __init__(self, user):
        """
        Initialize the PaymentService with the current user.

        Args:
            user (CustomUser): The authenticated user for whom the service acts.
        """
        self.user = user

    def validate_pay_method(self, method: str) -> bool:
        """
        Check if the provided payment method is supported.

        Args:
            method (str): The payment method to validate.

        Returns:
            bool: True if supported, False otherwise.
        """
        try:
            PaymentMethod(method)  # try to cast
            return True
        except ValueError:
            return False

    def save_method_to_order(self, order: Order, method: str) -> None:
        """
        Save the selected payment method to the order.

        Args:
            order (Order): The order instance to update.
            method (str): The selected payment method.

        Raises:
            ValueError: If the method is not supported.
        """
        if not self.validate_pay_method(method):
            raise ValueError(f"Invalid payment method: {method}")
        # Assuming order has a field 'payment_method' to store the selected method
        order.payment_method = method
        order.save()

    def get_supported_methods(self) -> list[str]:
        """
        Return all supported payment methods.

        Returns:
            List[str]: A list of valid payment method strings.
        """
        return [method.value for method in PaymentMethod]

    def process_payment(
        self,
        amount: float,
        method: str,
        order: Order,
        success_url=None,
        cancel_url=None,
    ) -> dict:
        provider_class = PROVIDER_MAP.get(method)
        if not provider_class:
            return {"status": "unsupported", "message": "Unsupported method."}

        provider = provider_class(self.user, order)

        if hasattr(provider, "create_checkout_session"):
            url = provider.create_checkout_session(success_url, cancel_url)
            return {"status": "ok", "redirect_url": url}
        else:
            return {
                "status": "unsupported",
                "message": "Provider does not support checkout.",
            }
