from django.core.mail import send_mail

from celery import shared_task

from orders.models import Order


@shared_task
def order_created(order_id):
    """ Отправляем email, если заказ был успешно создан"""

    order = Order.objects.get(id=order_id)
    subject = f"Номер заказа: {order.id}"
    message = "Привет {},\n\nВаш заказ был успешно создан и отправлен на обработку.\
               Номер вашего заказа {}.".format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, 'admin@secdet.com', [order.email])
    return mail_sent
