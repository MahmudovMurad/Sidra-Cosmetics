import base64
import hmac
import hashlib
import requests
import json
import random
import uuid
from django.conf import settings
from dataclasses import dataclass
from django.utils.module_loading import import_string
from apps.orders.models import Order


@dataclass
class Akbank:
    merchant_id: str
    merchant_key: str
    merchant_salt: str

    def create_link(self, order: Order):

        transaction_uuid = uuid.uuid4()
        order.transaction = transaction_uuid
        order.save()

        # Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.
        name = f"Order transaction={str(transaction_uuid)}"

        # 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)
        price = str(order.total_price * 100)

        # TL - USD - EUR - GBP gönderilebilir.
        currency = "TL"

        # 2 - 12 arası gönderilebilir. 1 gönderilirse bireysel kartlar taksit yapılamaz.
        max_installment = '1'

        # collection (fatura/cari tahsilat) veya product (ürün/hizmet satışı) gönderilebilir.
        # collection ise email (ödeme yapan tarafın eposta adresi olmalı).
        # product ise min_count (satın alma adet alt limiti) gereklidir.
        link_type = 'product'

        # tr veya en gönderilebilir.
        lang = 'tr'

        # Opsiyoneldir 1 veya 0 gönderilebilir. 1 gönderildiğinde yanıt içerisinde
        # QR kod oluşturabilmeniz için PNG formatında Base64 kodu döner.
        get_qr = 0

        min_count = 1
        email = ""

        required = name + price + currency + max_installment + link_type + lang + min_count

        callback_link = 'http://64.226.106.186/payments/akbank/callback/'
        callback_id = str(transaction_uuid)
        debug_on = 1

        hash_str = required + self.merchant_salt
        paytr_token = base64.b64encode(hmac.new(self.merchant_key, hash_str.encode(), hashlib.sha256).digest())

        params = {
            'merchant_id': self.merchant_id,
            'name': name,
            'price': price,
            'currency': currency,
            'max_installment': max_installment,
            'link_type': link_type,
            'lang': lang,
            'min_count': min_count,
            'email': email,
            'callback_link': callback_link,
            'callback_id': callback_id,
            'debug_on': debug_on,
            'get_qr': get_qr,
            'paytr_token': paytr_token,
        }

        result = requests.post('https://www.paytr.com/odeme/api/link/create', params)
        res = json.loads(result.text)

        if res['status'] == 'error':
            print('Error: ' + res['err_msg'])

            order.status = "error"
            order.save()

            raise ValueError(res['err_msg'])
        elif res['status'] == 'failed':

            order.status = "failed"
            order.save()

            print(result.text)
            raise ValueError(result.text)
        else:
            print(result.text)
            return result.text



akbank_payment_gateway: Akbank = import_string(settings.AKBANK["BACKEND"])(
    **settings.AKBANK["OPTIONS"]
)