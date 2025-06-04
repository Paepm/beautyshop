import requests
from django.conf import settings
from devtools import debug


class QogitaClient:
    def __init__(self):
        self.access_token = None
        self.base_url = "https://api.qogita.com"
        self.qogita_email = settings.QOGITA_EMAIL
        self.qogita_pw = settings.QOGITA_PASSWORD

    def authorisation_api(self):

        authorisation_url = f"{self.base_url}/auth/login"
        print("POST to:", authorisation_url)

        response = requests.post(
            url=authorisation_url,
            json={"email": self.qogita_email, "password": self.qogita_pw},
            headers={"Content-Type": "application/json"},
        )

        debug("Status Code:", response.status_code)
        debug("Raw Text:", response.text)
        if response.status_code != 200:
            raise Exception(f"Failed to authenticate: {response.text}")
        data = response.json()
        debug("Response JSON:", data)

        self.access_token = data["accessToken"]
        # headers = {"Authorization": f"Bearer {access_token}"}
        cart_qid = data["user"]["activeCartQid"]
