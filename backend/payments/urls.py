from django.urls import path

from payments.views import checkout_views
from payments.views import webhook_views


app_name = "payments"

urlpatterns = [
    path(
        "create/",
        checkout_views.select_payment_provider_view,
        name="select_payment_provider",
    ),
    path("stripe/", checkout_views.start_payment_view, name="start_payment"),
    path("error/", checkout_views.error_payment_view, name="error_payment"),
    path("webhook/stripe/", webhook_views.stripe_webhook_view, name="stripe_webhook"),
    path("cancel/", checkout_views.cancel_payment_view, name="cancel_payment"),
    path("webhook/paypal/", webhook_views.paypal_webhook_view, name="paypal_webhook"),
]
