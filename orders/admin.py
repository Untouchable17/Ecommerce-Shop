from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'phone',
        'email',
        'address',
        'status',
        'buying_type',
        'created_at'
    ]
    list_filter = ['status', 'buying_type', 'created_at']
    inlines = [OrderItemInline]