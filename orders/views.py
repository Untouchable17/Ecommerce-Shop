from django.shortcuts import render, redirect
from django.urls import reverse

from orders.models import OrderItem
from orders.forms import OrderCreateForm
from orders.tasks import order_created
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm()
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            try:
                order.cart_owner = request.user
            except: pass
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.coupon_discount
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])

            # обнуляем корзину
            cart.clear()

            # отправка SMTP через CELERY
            order_created.delay(order.id)
            request.session['order_id'] = order.id

            return redirect(reverse("payment:process"))

            # на случай, если надо убрать/заменить платежную систему
            # context = {'order': order}
            # return render(request, 'orders/order_created.html', context)

    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


