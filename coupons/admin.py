from django.contrib import admin

from coupons.models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'coupon_code',
        'coupon_valid_form',
        'coupon_valid_to',
        'coupon_discount',
        'coupon_active'
    ]
    list_filter = [
        'coupon_active',
        'coupon_valid_form',
        'coupon_valid_to'
    ]
    search_fields = ['coupon_code']


admin.site.register(Coupon, CouponAdmin)