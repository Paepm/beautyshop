from enum import Enum


class PaymentMethodType(str, Enum):
    CARD: str = "card"
    PAYPAL: str = "paypal"
    APPLE_PAY: str = "apple_pay"
    GOOGLE_PAY: str = "google_pay"
    KLARNA: str = "klarna"
    BANK_TRANSFER: str = "bank_transfer"
