from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from devtools import debug

from payments.services.checkout_service import CheckoutService


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            shipping_data = data.get("shipping_data", {})
            # debug("[CHECKOUT_VIEW] Shipping data received:", shipping_data)
            debug("[CHECKOUT_VIEW] Data received:", data)
            payment_provider = data.get("payment_provider")
            payment_method = data.get("payment_method")

            # debug("[CHECKOUT_VIEW] Data received:", data)

            # debug("[CHECKOUT_VIEW]paymentprovider:", payment_provider)
            # debug("[CHECKOUT_VIEW]shipping_data:", shipping_data)
            # debug("[CHECKOUT_VIEW]payment_method:", payment_method)

            checkout = CheckoutService(user)
            checkout.create_order(
                payment_provider=payment_provider,
                shipping_data=shipping_data,
                payment_method=payment_method,
            )
            checkout.save_shipping_info(shipping_data, payment_method)

            debug("[CHECKOUT_VIEW] Order created successfully:", checkout.order)

            success_url = (
                f"http://localhost:3000/payments/success_payment/{checkout.order.id}"
            )
            cancel_url = "http://localhost:3000/payments/cancel_payment"

            redirect_url = checkout.start_checkout(success_url, cancel_url)
            return Response({"redirect_url": redirect_url}, status=status.HTTP_200_OK)

        except ValueError as ve:
            debug("[CHECKOUT_VIEW] ValueError during checkout:", str(ve))
            return Response({"detail": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            debug("[CHECKOUT_VIEW] Error during checkout:", str(e))
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
