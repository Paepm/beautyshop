from payments.enums.payment_methods import PaymentMethod
from payments.services.providers.stripe_provider import StripeProvider
from payments.services.providers.paypal_provider import PayPalProvider


PROVIDER_MAP = {
    PaymentMethod.CARD.value: StripeProvider,
    PaymentMethod.PAYPAL.value: PayPalProvider,
}
