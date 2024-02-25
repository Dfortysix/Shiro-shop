from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from carts.models import Cart, CartItem
from category.models import Category
from carts.views import _cart_id


def store(request, category_slug=None):
    query = request.GET.get("q", "")
    all_categories = Category.objects.all()
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
    if query:
        products = Product.objects.filter(Q(product_name__icontains=query) | Q(product_name__icontains=query.capitalize()) | Q(product_name__icontains=query.upper()) | Q(description__icontains=query))

    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 3)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'categories': all_categories
    }
    return render(request, 'store/store.html', context=context)


def product_detail(request, category_slug, product_slug=None):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        in_cart = CartItem.objects.filter(
            cart=cart,
            product=single_product
        ).exists()
    except Exception as e:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )

    context = {
        'single_product': single_product,
        'in_cart': in_cart if 'in_cart' in locals() else False,
    }
    return render(request, 'store/product_detail.html', context=context)


