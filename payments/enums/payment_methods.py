from enum import Enum


class PaymentMethod(str, Enum):
    STRIPE = 'stripe'
    CARD = 'card'
    PAYPAL = 'paypal'
    INVOICE = 'invoice'
    BANK_TRANSFER = 'bank_transfer'
    CRYPTO = 'crypto'
    KLARA = 'klara'
    