from payments.enums.payment_methods import PaymentMethod
from payments.services.providers.stripe_provider import StripeProvider


PROVIDER_MAP = {
    PaymentMethod.STRIPE.value: StripeProvider,
    # Add other payment providers here
    }