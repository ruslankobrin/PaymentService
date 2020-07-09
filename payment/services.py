import requests
from flask import redirect, render_template

from app.config import SHOP_ID, PAYWAY
from payment.utils import generate_sign


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

        response = requests.post(url, json=data)
        response = response.json()

        if response['result']:
            url_for_redirect = response['data']['url']
            return url_for_redirect

        else:
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
        response = requests.post(url, json=data)
        response = response.json()
        if response['result']:
            invoice_data = {
                "url": response['data']['url'],
                "lang": "ru",
                "m_curorderid": response['data']['data']['m_curorderid'],
                "m_historyid": response['data']['data']['m_historyid'],
                "m_historytm": response['data']['data']['m_historytm'],
                "referer": response['data']['data']['referer'],
                "method": response['data']['method'],
            }
            return invoice_data
        else:
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