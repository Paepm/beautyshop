from orders.models import Order

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
        return self.ALLOWED_METHODS