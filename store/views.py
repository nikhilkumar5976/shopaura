from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import Cartitem
from django.db.models import Q
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# ==============================================================================
# Store & Product Views
# ==============================================================================

def store(request, category_slug=None):
    """
    Render the main product catalog / store page.
    - If category_slug is provided, filters available products belonging to that category.
    - Otherwise, returns all available products in the catalog.
    - Applies pagination (6 items per page) using Django's Paginator.
    """
    categories = None
    products = None

    if category_slug != None:
        # Filter products by selected category
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        # Display all available products across all categories
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    """
    Render the single product detail page.
    - Retrieves the product using category slug and product slug.
    - Verifies whether this product is already in the visitor's cart (via session cart ID).
    """
    try:
        # Fetch product matching both category slug and product slug
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # Check if product is already added in the current session's cart
        in_cart = Cartitem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product-detail.html', context)


def search(request):
    """
    Handle product search queries from the navbar search bar.
    - Reads the 'keyword' GET parameter.
    - Performs case-insensitive matching across product name and description using Q lookups.
    - Orders matched items by newest created date first.
    """
    products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Search product name OR description containing the keyword
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

