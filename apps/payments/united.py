import requests
from dataclasses import dataclass
from django.utils.module_loading import import_string
from django.conf import settings
from apps.payments.models import Transaction
from apps.orders.models import Order


@dataclass
class UnitedPayment:
    BASE_URL: str
    LOGIN_EMAIL: str
    LOGIN_PASSWORD: str
    SUCCESS_URL: str
    CANCEL_URL: str
    DECLINE_URL: str

    def _prepare_headers(self, token: str | None = None) -> dict:
        header = {
            "Content-Type": "application/json",
        }
        if token:
            header["x-auth-token"] = token

        return header

    def create_transaction(self, order: Order, order_id: str, amount: float, description: str, transaction_id: str):
        Transaction.objects.create(
            user_ip=order.user_ip,
            order=order,
            order_uuid=order_id,
            transaction_uuid=transaction_id,
            description=description,
            amount=amount,
        )

    def get_token(self):
        headers = self._prepare_headers()
        url = f"{self.BASE_URL}/auth/"
        payload = {
            "email": self.LOGIN_EMAIL,
            "password": self.LOGIN_PASSWORD,
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()["token"]

    def checkout(
        self,
        order: Order,
        order_uuid: str | int,
        amount: float,
        description: str,
        language: str = "AZ",
    ):
        url = f"{self.BASE_URL}/transactions/checkout"

        headers = self._prepare_headers(token=self.get_token())

        payload = {
            "clientOrderId": order_uuid,
            "amount": amount,
            "language": language,
            "description": description,
            "successUrl": self.SUCCESS_URL,
            "cancelUrl": self.CANCEL_URL,
            "declineUrl": self.DECLINE_URL,
        }
        response = requests.post(url, headers=headers, json=payload)

        pay_url = response.json()["url"]
        transaction_id = response.json()["transactionId"]

        self.create_transaction(
            order=order,
            order_id=order_uuid,
            transaction_id=transaction_id,
            amount=amount,
            description=description,
        )
        return pay_url


united_payment_gateway: UnitedPayment = import_string(settings.UNITED_PAYMENT["BACKEND"])(
    **settings.UNITED_PAYMENT["OPTIONS"]
)