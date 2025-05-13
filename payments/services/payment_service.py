from orders.models import Order
from payments.services.providers.stripe_provider import StripeProvider
from payments.enums.payment_methods import PaymentMethod

class PaymentService:
    """Handles payment logic methods and processes payments for orders."""

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
    
    def save_method_to_order(self, order:Order, method:str) -> None:
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

    def process_payment(self, amount: float, method: str) -> dict:
        """
        Process the payment using the selected method.

        Args:
            amount (float): The amount to be charged.
            method (str): The payment method (e.g. 'stripe').

        Returns:
            dict: A dictionary with payment status and optional provider info.
        """
        if method == 'stripe':
            provider = StripeProvider(self.user)
            return provider.create_payment_intent(amount, currency='eur')
        
        # placeholder for other payment methods
        return {'status': 'unsupported',
                'message': f'This payment method {method} is not yet implemented.'}
