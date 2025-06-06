import io
import csv
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class OrderExportService:
    """
    Handles exporting orders to CSV and PDF format.
    """

    def export_csv(self, orders):
        """
        Export orders as CSV response.
        """
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        # Header row
        writer.writerow(
            ["ID", "User", "Total (€)", "Payment Status", "Order Status", "Date"]
        )

        # Order rows
        for o in orders:
            writer.writerow(
                [
                    o.id,
                    o.user.username,
                    f"{o.total_price:.2f}",
                    o.payment_status,
                    o.order_status,
                    o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

        # Build response
        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="orders.csv"'
        return response

    def export_pdf(self, orders):
        """
        Export orders as a nicely styled table-based PDF.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("Orders Report", styles["Heading2"]))
        elements.append(Spacer(1, 12))

        # Table data: Header + Rows
        data = [
            [
                "Order ID",
                "Username",
                "Total (€)",
                "Payment Status",
                "Order Status",
                "Created Date",
            ]
        ]
        total_sum = 0

        for o in orders:
            data.append(
                [
                    str(o.id),
                    o.user.username,
                    f"{o.total_price:.2f}",
                    o.payment_status,
                    o.order_status,
                    o.created_at.strftime("%d.%m.%Y, %H:%M"),
                ]
            )
            total_sum += float(o.total_price)

        # Add total sum row
        data.append(["", "Total", f"{total_sum:.2f} €", "", "", ""])

        # Table setup
        table = Table(data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                ]
            )
        )

        elements.append(table)

        # Build PDF
        doc.build(elements)

        response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="orders.pdf"'
        return response
