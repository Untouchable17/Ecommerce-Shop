from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.utils import timezone

from coupons.models import Coupon
from coupons.forms import CouponeApplyForm


@require_POST
def coupon_apply(request):
    """ Применение купона """

    now = timezone.now()
    form = CouponeApplyForm(request.POST)
    if form.is_valid():
        coupon_code = form.cleaned_data['coupon_code']
        try:
            coupon = Coupon.objects.get(
                coupon_code__iexact=coupon_code,
                coupon_valid_form__lte=now,
                coupon_valid_to__gte=now,
                coupon_active=True
            )

            request.session['coupon_id'] = coupon.id

        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('cart:cart_detail')
