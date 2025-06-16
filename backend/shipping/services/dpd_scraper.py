import requests
from bs4 import BeautifulSoup
from datetime import datetime
from orders.models import Order


class DPDTrackingScraper:
    BASE_URL = "https://tracking.dpd.de/status/de_DE/parcel/"

    def fetch_tracking_status(self, tracking_id):
        url = f"{self.BASE_URL}{tracking_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Request failed for {tracking_id}: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        status_element = soup.select_one(".parcel-delivery-status span")

        if status_element:
            return status_element.text.strip().lower()

        return None

    def run(self):
        delivered = []
        in_transit = []
        failed = []

        orders = Order.objects.filter(
            order_status="shipped",
            shipping_provider="DPD",
            tracking_id="06215240100641",
        )

        print(f"🔍 Checking {orders.count()} shipped DPD orders...")

        for order in orders:
            status = self.fetch_tracking_status(order.tracking_id)

            if status is None:
                print(f"❌ No status found for Order #{order.id}.")
                failed.append(order.id)
                continue

            if "zugestellt" in status or "delivered" in status:
                order.order_status = "delivered"
                order.delivered_at = datetime.now()
                order.save()
                print(f"✅ Order #{order.id} marked as delivered.")
                delivered.append(order.id)
            else:
                print(f"⏳ Order #{order.id} not yet delivered (status: {status})")
                in_transit.append(order.id)

        return {
            "delivered": delivered,
            "in_transit": in_transit,
            "failed": failed,
        }
