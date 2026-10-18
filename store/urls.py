from django.urls import path
from . import views

# ==============================================================================
# Store URL Patterns
# ==============================================================================

urlpatterns = [
    # Full catalog view
    path('', views.store, name='store'),
    # Products filtered by category slug
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    # Single product detail view matching category and product slugs
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='products_detail'),
    # Product search results view
    path('search/', views.search, name='search'),
]