# payments/services/payment_dispatcher.py

from payments.services.provider_registry import PROVIDER_MAP
from devtools import debug


class PaymentDispatcher:
    def __init__(self, order, payment_method: str):
        self.order = order
        self.payment_method = payment_method
        self.provider_key = order.payment_provider

    def dispatch(self, success_url: str, cancel_url: str) -> str:
        debug(f"[DISPATCHER] Provider: {self.provider_key}")

        provider_class = PROVIDER_MAP.get(self.provider_key)
        if not provider_class:
            raise ValueError(f"Unsupported payment provider: {self.provider_key}")

        provider_instance = provider_class(user=self.order.user, order=self.order)

        if not hasattr(provider_instance, "create_checkout_session"):
            raise NotImplementedError(f"{self.provider_key} does not support checkout.")

        return provider_instance.create_checkout_session(success_url, cancel_url)
