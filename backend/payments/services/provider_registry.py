from payments.enums.payment_providers import PaymentProviders
from payments.services.providers.stripe_provider import StripeProvider
from payments.services.providers.paypal_provider import PayPalProvider


PROVIDER_MAP = {
    PaymentProviders.STRIPE.value: StripeProvider,
    PaymentProviders.PAYPAL.value: PayPalProvider,
}
