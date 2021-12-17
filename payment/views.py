import os

from django.shortcuts import redirect, get_object_or_404
from cloudipsp import Api, Checkout

from orders.models import Order


def payment_process(request):
    """ Передаем итоговую цену в платежную систему для оформления заказа """

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    api = Api(merchant_id=os.environ.get("PAYMENT_MERCHANT_ID"),
              secret_key=os.environ.get("PAYMENT_SECRET_KEY"))

    checkout = Checkout(api=api)

    data = {
        "currency": "USD",
        "amount": int(float(order.get_total_cost()))
    }

    url = checkout.url(data).get('checkout_url')

    return redirect(url)
