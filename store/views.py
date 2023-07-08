from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from carts.models import CartItem
from carts.views import _cart_id
from .models import Product
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        # Tìm trong db Category nếu slug=category_slug thì trả về sản phẩm, Nếu không phải trả về 404
        categories = get_object_or_404(Category, slug=category_slug)

        products = Product.objects.all().filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products =paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        '''
        category__slug được hiểu là đang truy vấn tới slug của Category thông qua quan hệ category
        tức là category__slug là đang gọi đến slug của model category  
        '''

        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) |
                Q(product_name__icontains= keyword))
            # __icontains: là một cách tìm kiếm trong Django được sử dụng để so sánh chuỗi một cách không phân biệt chữ hoa/chữ thường trong câu truy vấn cơ sở dữ liệu.
            # Q là một đối tượng được sử dụng để xây dựng các điều kiện truy vấn phức tạp. Nó cho phép bạn tạo ra các biểu thức truy vấn logic AND, OR, NOT để tìm kiếm dữ liệu trong cơ sở dữ liệu.
            product_count = products.count()

        context = {
            'products': products,
            'product_count': product_count,
        }
    return render(request, 'store/store.html', context)

