from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

from decimal import Decimal
import simplejson

from shop_app.models import Product
from coupons.models import Coupon


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ получен покупателем')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    coupon = models.ForeignKey(
        Coupon, related_name='orders',
        null=True, blank=True, on_delete=models.SET_NULL
    )

    cart_owner = models.OneToOneField(User, related_name="cart_owner", blank=True, null=True, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    order_id = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=70, verbose_name="Имя покупателя")
    last_name = models.CharField(max_length=70, verbose_name="Фамилия покупателя")
    phone = models.CharField(max_length=30, verbose_name="Номер телефона покупателя")
    email = models.CharField(max_length=70, verbose_name="Email покупателя")
    address = models.TextField(max_length=1200, verbose_name="Адрес покупателя")
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name="Статус заказа")
    buying_type = models.CharField(max_length=120, choices=BUYING_TYPE_CHOICES, verbose_name="Тип заказа")
    comment = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Комментарий к заказу")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    order_date = models.DateTimeField(default=timezone.now, verbose_name="Дата получения заказа")

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        convert_json = simplejson.dumps(total_cost - total_cost * (self.discount / Decimal('100')))
        return convert_json

    def __str__(self):
        return f'Order {self.id} | {self.first_name} {self.last_name}'

    class Meta:
        ordering = ('-created_at', )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.id}"