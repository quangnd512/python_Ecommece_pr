from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Product, Variation


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
                # print(variation)
            except:
                pass


        # color = request.GET['color']
        # size = request.GET['size']

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()

    return redirect('cart')


class ObjectNotExist:
    pass

# Các tham số truyền vào mặc định là 0 và None
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        #Lấy tất cả request của Cart với cart_id = _cart_id ở trên
        cart = Cart.objects.get(cart_id=_cart_id(request))

        # Lấy tất cả request của CartItem nếu cart trùng cart được khai báo ở trên và nó có is_active = True
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        tax = 0
        grand_total = 0

        #Lăp qua tất cả các cart_item tìm được
        for cart_item in cart_items:
            # Tổng số tền của sản phẩm
            total += (cart_item.product.price * cart_item.quantity )

            # Tổng số sản phẩm
            quantity += cart_item.quantity

            # Thuế: 1,5% tổng số tiền của sản phẩm
            tax = (total*2)/100

            # Số tiền thực trả: tổng + thuế
            grand_total = total + tax
    except ObjectNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    # Trả các data về store/cart.html
    return render(request, 'store/cart.html', context)


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id= _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')
