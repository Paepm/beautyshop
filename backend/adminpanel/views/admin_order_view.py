from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from devtools import debug

from adminpanel.service.permissions import IsSuperUser
from adminpanel.service.admin_order_service import AdminOrderService
from adminpanel.serializers.serializers import AdminOrderSerializer
from orders.models import Order
from adminpanel.service.admin_order_export_service import OrderExportService


class AdminOrderListView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        serializer = AdminOrderService().get_all_orders(filters=request.GET)
        return Response(serializer, status=status.HTTP_200_OK)


class AdminOrderDetailView(APIView):

    permission_classes = [IsSuperUser]

    def get(self, request, pk):
        try:
            serializer = AdminOrderService().get_order_by_id(order_id=pk)
            return Response(serializer)
        except Order.DoesNotExist:
            return Response({"error": "Not found"}, status=404)


class AdminOrderExportView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        export_format = request.query_params.get("file_format")
        orders = AdminOrderService().get_queryset(request.GET)
        exporter = OrderExportService()

        if export_format == "csv":
            return exporter.export_csv(orders)
        elif export_format == "pdf":
            return exporter.export_pdf(orders)

        return Response({"error": "Ungültiges Format"}, status=400)
