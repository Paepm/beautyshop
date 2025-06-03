from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from devtools import debug


from orders.services.order_creator import OrderCreator
from payments.services.payment_dispatcher import PaymentDispatcher


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        shipping_data = data.get("shipping_data", {})
        shipping_method = data.get("shipping_method")
        payment_provider = data.get("payment_provider")
        payment_method = data.get("payment_method")
        debug("[CHECKOUTVIEW] Received data:", data)

        # 1. Bestellung erstellen
        order_creator = OrderCreator(user)
        order = order_creator.create_order(payment_provider=payment_provider)
        debug("[CHECKOUTVIEW] Order created:", order)

        if not order:
            debug("[CHECKOUTVIEW] Order creation failed.")
            return Response(
                {"detail": "Order creation failed."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Adresse und Methode speichern
        order.shipping_address = f"{shipping_data.get('address', '')}, {shipping_data.get('post_code', '')} {shipping_data.get('city', '')}, {shipping_data.get('country', '')}"
        debug("[CHECKOUTVIEW] Shipping address set to:", order)
        order.payment_method = payment_method
        order.save()

        # 3. PaymentService wählen
        dispatcher = PaymentDispatcher(order=order, payment_method=payment_method)
        debug(
            "[CHECKOUTVIEW] Dispatching payment service for provider:", payment_provider
        )

        success_url = f"http://localhost:3000/payments/success_payment/{order.id}"
        cancel_url = f"http://localhost:3000/payments/cancel_payment/{order.id}"

        try:
            redirect_url = dispatcher.dispatch(
                success_url=success_url, cancel_url=cancel_url
            )
            debug("[CHECKOUTVIEW] Redirect URL from payment service:", redirect_url)
            return Response({"redirect_url": redirect_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
