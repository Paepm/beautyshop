from payments.services.providers.stripe_provider import StripeProvider
from payments.services.providers.paypal_provider import PayPalProvider
from payments.enums.payment_providers import PaymentProviders
from devtools import debug


class PaymentDispatcher:
    def __init__(self, order, payment_method: str):
        self.order = order
        self.payment_method = payment_method
        self.provider = order.payment_provider

    def dispatch(self, success_url: str, cancel_url: str):
        debug("im here hello")
        if self.provider == PaymentProviders.STRIPE.value:
            return StripeProvider(
                user=self.order.user, order=self.order
            ).create_checkout_session(success_url, cancel_url)

        elif self.provider == PaymentProviders.PAYPAL.value:
            return PayPalProvider(
                user=self.order.user, order=self.order
            ).create_checkout_session(success_url, cancel_url)

        raise ValueError(f"Unsupported payment provider: {self.provider}")
