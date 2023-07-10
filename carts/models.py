from django.db import models
from store.models import Product, Variation


# Create your models here.
class Cart(models.Model):
    DoesNotExist = None
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ## new 12 - Them dòng sau
    variations = models.ManyToManyField(Variation, blank=True)
    # Sau đó dùng lệnh: python manage.py makemigrations
    # Và lệnh: python manage.py migrate
    ## new 12
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    ## new 12 - Sửa __str__
    def __unicode__(self):
        return self.product
    ## new 12

