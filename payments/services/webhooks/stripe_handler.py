from devtools import debug

from orders.models import Order

class StripeWebhookHandler:

    def __init__(self, request):
        self.request = request

    def handle(self, event):
        event_type = event['type']
        method = getattr(self, f'handle_{event_type.replace(".", "_")}', self.handle_default)
        return method(event)
    
    def handle_payment_intent_succeeded(self, event):
        intent = event['data']['object']
        user_id = intent['metadata'].get('user_id')
        debug(f"PaymentIntent was successful for user {user_id}!")
        # Mark order as paid
        if user_id:
            try:
                order = Order.objects.filter(user_id=user_id, payment_status='open').latest('created_at')
                order.payment_status = 'paid'
                debug("order_status:", order.payment_status)
                order.save()
            except Order.DoesNotExist:
                debug(f'No open order found for user {user_id}.')
        else:
            debug('No user ID found in metadata.')

        return "Handled: payment_intent.succeeded"
    
    def handle_payment_intent_payment_failed(self, event):
        intent = event['data']['object']
        user_id = intent['metadata'].get('user_id')
        error_message = intent.get("last_payment_error",{}).get('message', 'Unknown error')

        debug(f'Payment failed: {user_id} - {error_message}')

        if user_id:
            try:
                order = Order.objects.filter(user_id=user_id, payment_status='open').latest('created_at')
                order.payment_status = 'failed'
                order.save()
                debug("order_status:", order.payment_status)
            except Order.DoesNotExist:
                debug(f'No open order found for user {user_id}.')
        else:
            debug('No user ID found in metadata.')
            
        return "Handled: payment_intent.payment_failed"
        
    def handle_default(self, event):
        debug(f"Unhandled event type: {event['type']}")
        return "Ignored"
    
