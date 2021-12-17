from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from coupons.forms import CouponeApplyForm
from cart.forms import CartAddProductForm
from shop_app.models import Product
from cart.cart import Cart


@require_POST
def cart_add(request, product_id):
    """ Добавление товара в корзину """

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """ Удаление товара из корзины """

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_detail(request):
    """ Просмотр товаров в корзине """

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True}
        )

    coupon_apply_form = CouponeApplyForm()

    context = {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form,
    }

    return render(request, 'cart/cart_detail.html', context)
