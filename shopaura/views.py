from django.shortcuts import render
from store.models import Product, ReviewRating

# ==============================================================================
# Home View
# ==============================================================================

def home(request):
    """
    Render the homepage of the ShopAura store.
    Fetches all available products to display in the 'Popular Products' section.
    """
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)