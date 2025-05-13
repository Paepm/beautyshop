# payments/providers/stripe_provider.py
from decouple import config
import stripe

class StripeProvider:

    def __init__(self, user):
        self.user = user
        stripe.api_key = config('STRIPE_SECRET_KEY') # load the key from .env file

    def create_payment_intent(self, amount: float, currency: str = 'eur') -> dict:
      intent = stripe.PaymentIntent.create(
          amount=int(amount * 100), # stripe expects cents
          currency=currency,
          metadata={
              'user_id': self.user.id,
              'email': self.user.email,
          }
      )
      return {
          'payment_intent_id': intent.id,
          'client_secret': intent.client_secret,
          'amount': amount,
          'currency': currency,
          'status': intent.status,
      }
    
    
    # DUMMY METHODS TO SIMULATE PAYMENT CONFIRMATION AND CANCELLATION
    def confirm_payment(self, payment_intent_id: str) -> bool:
        """
        Dummy confirm logic. In real world, check payment status from Stripe API.
        """
        # Simulate a successful confirmation
        return True

    def cancel_payment(self, payment_intent_id: str) -> bool:
        """
        Dummy cancel logic. Real implementation would call Stripe's cancel API.
        """
        return True
