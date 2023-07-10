from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

## new 12 - Thêm các dòng sau
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')
## new 12

admin.site.register(Cart)
admin.site.register(CartItem)
