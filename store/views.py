from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.models import Cartitem
from django.db.models import Q

from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct

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

    if request.user.is_authenticated:
        try:
            orderproduct=OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct=None

    else:
        orderproduct=None

    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)
    product_gallery=ProductGallery.objects.filter(product_id=single_product.id)


    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallery':product_gallery,
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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)