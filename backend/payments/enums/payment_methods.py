from enum import Enum


class PaymentMethodTypes(str, Enum):
    CARD: str = "card"
    SOFORT: str = "sofort"
    BANCONTACT: str = "bancontact"
    SEPA_DEBIT: str = "sepa_debit"
    KLARNA: str = "klarna"
