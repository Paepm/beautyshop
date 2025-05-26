from enum import Enum


class PaymentProviders(str, Enum):
    STRIPE = "stripe"
    PAYPAL = "paypal"

    @property
    def label(self) -> str:
        return {
            self.STRIPE: "Stripe",
            self.PAYPAL: "PayPal",
        }[self]
