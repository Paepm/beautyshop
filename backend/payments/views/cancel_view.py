# payments/views/cancel_view.py
from django.shortcuts import redirect
from django.views import View
from devtools import debug


class PaymentCancelView(View):
    def get(self, request, order_id):
        debug(f"[CANCEL_VIEW] Payment canceled for order #{order_id}")
        return redirect(f"http://localhost:3000/payments/cancel_payment/{order_id}/")
