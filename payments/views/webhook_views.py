import stripe
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from devtools import debug

from payments.services.webhooks.stripe_handler import StripeWebhookHandler


@csrf_exempt
def stripe_webhook_view(request):
    """
    Stripe Webhook Endpoint - verifies signature and dispatches event
    """
    # get the json-webhook from stripe
    payload = request.body
    # safety header for verification
    sig_header = request.headers.get("stripe-signature")
    # secret key from .env
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        # construct_event() --> check if payload, header and secret is valid
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=endpoint_secret
        )
    except ValueError as e:
        debug("VALUE ERROR:", e)
        return HttpResponseBadRequest(f"Invalid payload: {e}")
    except stripe.error.SignatureVerificationError as e:
        debug("SIGNATURE ERROR:", e)
        return HttpResponseBadRequest(f"Invalid signature: {e}")

    # handle the event
    handler = StripeWebhookHandler(request)
    response = handler.handle(event)

    return HttpResponse(response or "OK")
