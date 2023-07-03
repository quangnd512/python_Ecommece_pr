from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        # Tìm trong db Category nếu slug=category_slug thì trả về sản phẩm, Nếu không phải trả về 404
        categories = get_object_or_404(Category, slug=category_slug)

        products = Product.objects.all().filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
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
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
    }

    return render(request, 'store/product_detail.html', context)