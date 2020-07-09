import requests
from flask import redirect, render_template

from app import app
from app.config import SHOP_ID, PAYWAY
from payment.utils import generate_sign

logger = app.logger

class PaymentServices:

    def __init__(self, amount, currency, description, shop_order_id):
        self.amount = amount
        self.currency = currency
        self.description = description
        self.shop_order_id = shop_order_id

    def pay(self):
        pay_data = {
            "currency": self.currency,
            "amount": self.amount,
            "shop_id": SHOP_ID,
            "shop_order_id": self.shop_order_id
        }
        sign = generate_sign(pay_data)
        pay_data['sign'] = sign
        pay_data['description'] = self.description
        pay_data['url'] = 'https://pay.piastrix.com/ru/pay'
        logger.info(f'Piastrix pay data: {pay_data}')
        return pay_data

    def bill(self):
        url = 'https://core.piastrix.com/bill/create'
        data = {
            "payer_currency": self.currency,
            "shop_amount": self.amount,
            "shop_currency": self.currency,
            "shop_id": SHOP_ID,
            "shop_order_id": self.shop_order_id
        }

        sign = generate_sign(data)
        data['sign'] = sign
        logger.info(f"Request for piastrix bill: {data}")

        response = requests.post(url, json=data)
        response = response.json()

        if response['result']:
            logger.info(f"Piastrix bill response: {response}")
            url_for_redirect = response['data']['url']
            return url_for_redirect

        else:
            logger.error(f'Error response during piastrix bill: {response}')
            print('Bad request for bill')

    def invoice(self):
        url = 'https://core.piastrix.com/invoice/create'
        data = {
            "amount": self.amount,
            "currency": self.currency,
            "payway": PAYWAY,
            "shop_id": SHOP_ID,
            "shop_order_id": self.shop_order_id,
        }

        sign = generate_sign(data)
        data['sign'] = sign
        logger.info(f"Request for piastrix invoice: {data}")

        response = requests.post(url, json=data)
        response = response.json()

        if response['result']:
            logger.info(f"Piastrix invoice response: {response}")
            invoice_data = {
                "url": response['data']['url'],
                "lang": "ru",
                "m_curorderid": response['data']['data']['m_curorderid'],
                "m_historyid": response['data']['data']['m_historyid'],
                "m_historytm": response['data']['data']['m_historytm'],
                "referer": response['data']['data']['referer'],
                "method": response['data']['method'],
            }
            logger.info(f'Piastrix invoice data: {invoice_data}')
            return invoice_data
        else:
            logger.info(f'Error response during piastrix invoice: {response}')
            print('Bad request for bill')

def get_piastrix_service(amount, currency, description, shop_order_id):
    return PaymentServices(amount, currency, description, shop_order_id)

def get_piastrix_action(piastrix, currency):
    if currency == '978':
        return render_template('pay.html', data=piastrix.pay())
    elif currency == '840':
        return redirect(piastrix.bill())
    elif currency == '643':
        return render_template('invoice.html', data=piastrix.invoice())
    else:
        print('Get invalid code currency')