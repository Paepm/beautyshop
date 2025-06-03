# payments/views/success_view.py
from django.shortcuts import redirect
from django.views import View
from devtools import debug


class PaymentSuccessView(View):
    def get(self, request, order_id):
        debug(f"[SUCCESS_VIEW] Payment successful for order #{order_id}")
        return redirect(f"http://localhost:3000/payments/success_payment/{order_id}/")
