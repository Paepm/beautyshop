import stripe
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from devtools import debug

from payments.services.webhooks.stripe_handler import StripeWebhookHandler
from payments.services.webhooks.paypal_handler import PayPalWebhookHandler


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.headers.get("stripe-signature")
    secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=secret
        )
    except ValueError as e:
        debug("Invalid Stripe payload:", e)
        return HttpResponseBadRequest(f"Invalid payload: {e}")
    except stripe.error.SignatureVerificationError as e:
        debug("Invalid Stripe signature:", e)
        return HttpResponseBadRequest(f"Invalid signature: {e}")

    handler = StripeWebhookHandler(request)
    response = handler.handle(event)
    return HttpResponse(response or "OK")


@csrf_exempt
def paypal_webhook_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    handler = PayPalWebhookHandler(request)
    response = handler.handle(payload)
    return HttpResponse(response, status=200)
