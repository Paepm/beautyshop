from payments.enums.payment_provider import PaymentProvider
from payments.services.providers.stripe_provider import StripeProvider
from payments.services.providers.paypal_provider import PayPalProvider


PROVIDER_MAP = {
    PaymentProvider.STRIPE.value: StripeProvider,
    PaymentProvider.PAYPAL.value: PayPalProvider,
}
