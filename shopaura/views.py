from django.shortcuts import render
from store.models import Product

# ==============================================================================
# Home View
# ==============================================================================

def home(request):
    """
    Render the homepage of the ShopAura store.
    Fetches all available products to display in the 'Popular Products' section.
    """
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request, 'home.html', context)