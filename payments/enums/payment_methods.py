from enum import Enum


class PaymentMethod(str, Enum):
    CARD = "card"
    PAYPAL = "paypal"

    def label(self) -> str:
        return {
            self.CARD: "Credit Card",
            self.PAYPAL: "PayPal",
        }
