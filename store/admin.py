from django.contrib import admin
from .models import Product, Variation


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(Product, ProductAdmin)

## new 12 đăng ký với admin Variation
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('s_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Variation)
## new 12
