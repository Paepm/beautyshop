from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from devtools import debug

from adminpanel.service.permissions import IsSuperUser
from adminpanel.service.admin_order_service import AdminOrderService
from adminpanel.serializers.serializers import AdminOrderSerializer

from orders.models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponse
import csv
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from orders.models import Order


class AdminOrderListView(APIView):
    """
    API View that returns all orders for admin users.
    """

    permission_classes = [IsSuperUser]

    def get(self, request):

        serializer = AdminOrderService().get_all_orders()

        debug("DATA", serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminOrderDetailView(APIView):

    permission_classes = [IsSuperUser]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = AdminOrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Not found"}, status=404)


class AdminOrderExportView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        format = request.GET.get("format")
        orders = Order.objects.all().select_related("user")

        if format == "csv":
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(["ID", "User", "Total", "Status", "Date"])
            for o in orders:
                writer.writerow(
                    [
                        o.id,
                        o.user.username,
                        o.total_price,
                        o.payment_status,
                        o.created_at,
                    ]
                )

            response = HttpResponse(buffer.getvalue(), content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="orders.csv"'
            return response

        elif format == "pdf":
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            y = 800
            p.setFont("Helvetica", 12)
            p.drawString(50, y, "Orders Report")
            y -= 30
            for o in orders:
                p.drawString(
                    50,
                    y,
                    f"#{o.id} | {o.user.username} | €{o.total_price} | {o.payment_status} | {o.created_at.strftime('%Y-%m-%d')}",
                )
                y -= 20
                if y < 50:
                    p.showPage()
                    y = 800
            p.save()
            buffer.seek(0)
            response = HttpResponse(buffer, content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="orders.pdf"'
            return response

        return Response({"error": "Ungültiges Format"}, status=400)
