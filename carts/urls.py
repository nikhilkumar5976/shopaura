from django.urls import path
from . import views

# ==============================================================================
# Cart URL Patterns
# ==============================================================================

urlpatterns = [
    # Render shopping cart page
    path('', views.cart, name='cart'),
    # Add product / increment quantity in cart
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    # Decrement product quantity in cart
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    # Remove product line item completely from cart
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
]