from enum import Enum


class PaymentProvider(str, Enum):
    STRIPE = "stripe"
    PAYPAL = "paypal"

    @property
    def label(self) -> str:
        return {
            self.STRIPE: "Stripe",
            self.PAYPAL: "PayPal",
        }[self]
