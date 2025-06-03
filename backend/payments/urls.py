from django.urls import path

from payments.views import webhook_views
from payments.views.checkout_view import CheckoutView
from payments.views.success_view import PaymentSuccessView
from payments.views.cancel_view import PaymentCancelView

app_name = "payments"

urlpatterns = [
    path(
        "checkout_start/",
        CheckoutView.as_view(),
        name="checkout_start",
    ),
    path(
        "success_payment/<int:order_id>/",
        PaymentSuccessView.as_view(),
        name="success_payment",
    ),
    path(
        "cancel_payment/",
        PaymentCancelView.as_view(),
        name="cancel_payment",
    ),
    path("webhook/stripe/", webhook_views.stripe_webhook_view, name="stripe_webhook"),
    path("webhook/paypal/", webhook_views.paypal_webhook_view, name="paypal_webhook"),
    # path(
    #     "create/",
    #     checkout_views_old.select_payment_provider_view,
    #     name="select_payment_provider",
    # ),
    # path("stripe/", checkout_views_old.start_payment_view, name="start_payment"),
    # path("error/", checkout_views_old.error_payment_view, name="error_payment"),
    # path("cancel/", checkout_views_old.cancel_payment_view, name="cancel_payment"),
]
