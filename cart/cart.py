from django.conf import settings
from decimal import Decimal

from shop_app.models import Product
from coupons.models import Coupon


class Cart:

    def __init__(self, request):
        """ Инициализация объекта корзины """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем в сессию пустую корзину
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # сейвим купон
        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        """ Проходим по товарам корзины и получаем объекты Product """
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ Возвращаем общее количество товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """ Возвращаем итовогую цену в корзине """
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """ Полная очистка корзины от товаров """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def add(self, product, quantity=1, update_quantity=False):
        """ Добавление товара или обновление его количества """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # Делаем метку, что сессия была изменена
        self.session.modified = True

    def remove(self, product):
        """ Удаление товара из корзины """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    @property
    def coupon(self):
        """ Возвращаем соответствующий объект купона (если он задан) """
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        """ Считываем размер скидки (если в атрибуте coupon_id) """
        if self.coupon:
            return (self.coupon.coupon_discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        """ Возвращаем итоговую цену с учетом скидки """
        return self.get_total_price() - self.get_discount()