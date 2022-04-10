from django.contrib import admin
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from store.models import OrderItem, Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    list_display = ('product__name', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantity', 'total')
    search_fields = ('id', 'user__username', 'product__name')
    inlines = [OrderItemInline]

    @admin.display(description=_('admin_order_quantity'))
    def quantity(self, obj):
        return 'hoho'
        # return str(obj.items.aggregate(qty=Sum('quantity'))['qty'])


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price')
    search_fields = ('product__name',)
