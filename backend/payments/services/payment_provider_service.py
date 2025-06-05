# payments/services/payment_provider_service.py

from payments.enums.payment_providers import PaymentProviders
from orders.models import Order


class PaymentProviderService:
    def __init__(self):
        pass

    def validate(self, provider: str) -> bool:
        try:
            PaymentProviders(provider)
            return True
        except ValueError:
            return False

    def save_to_order(self, order: Order, provider: str) -> None:
        if not self.validate(provider):
            raise ValueError(f"Invalid payment provider: {provider}")
        order.payment_provider = provider
        order.save(update_fields=["payment_provider"])

    def get_supported_providers(self) -> list[str]:
        return list(map(str, PaymentProviders))
