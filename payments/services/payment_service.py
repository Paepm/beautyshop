from orders.models import Order
from payments.services.providers.stripe_provider import StripeProvider

class PaymentService:
    ALLOWED_METHODS = ['card', 'paypal', 'invoice', 'bank_transfer', 'crypto', 'klara']

    def __init__(self, user):
        self.user = user

    def validate_pay_method(self, method:str) -> bool:
        return method in self.ALLOWED_METHODS
    
    def save_method_to_order(self, order:Order, method:str) -> None:
        if not self.validate_pay_method(method):
            raise ValueError(f"Invalid payment method: {method}")
        # Assuming order has a field 'payment_method' to store the selected method
        order.payment_method = method
        order.save()

    def get_supported_methods(self) -> list[str]:
        """Returns a list of all supported methods."""
        return self.ALLOWED_METHODS

    def process_payment(self, order: Order, amount: float, method: str) -> dict:
        if method == 'card':
            provider = StripeProvider(self.user)
            return provider.create_payment_intent(amount, currency='eur')
        # placeholder for othjer payment methods
        return {'status': 'unsupported', 'message': f'This payment method {method} is not yet implemented.'}

    def get_supported_methods(self) -> list[str]:
        return self.ALLOWED_METHODS