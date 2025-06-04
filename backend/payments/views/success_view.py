# payments/views/success_view.py
from rest_framework.response import Response
from rest_framework.views import APIView
from devtools import debug
from rest_framework.permissions import IsAuthenticated


class PaymentSuccessView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        debug(f"[SUCCESS_VIEW] Payment successful for order #{order_id}")
        return Response(f"http://localhost:3000/payments/success_payment/{order_id}/")
