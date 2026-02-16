import requests
import base64
import json
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

    def _decode_base64_json(self, data):
        # 1. Base64 formatından baytlara (bytes) çeviririk
        decoded_bytes = base64.b64decode(data)

        # 2. Baytları string formatına (utf-8) çeviririk
        decoded_string = decoded_bytes.decode('utf-8')

        # 3. String-i JSON (dictionary) obyektinə çeviririk
        json_object = json.loads(decoded_string)

        return json_object

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

    def handle_checkout(
        self,
        data: str
    ):
        result = self._decode_base64_json(data)

        order_id = result["OrderId"]

        try:
            transaction = Transaction.objects.get(order_uuid=order_id)
        except Order.DoesNotExist:
            return False

        status = result["Status"]

        if status != "APPROVED":
            return False

        transaction.result_json = result
        transaction.is_completed = True
        transaction.save()

        order = transaction.order

        order.is_paid = True
        order.is_completed = True
        order.save()

        return True



united_payment_gateway: UnitedPayment = import_string(settings.UNITED_PAYMENT["BACKEND"])(
    **settings.UNITED_PAYMENT["OPTIONS"]
)