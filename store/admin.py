from django.contrib import admin
from .models import Product, Variation

# ==============================================================================
# Store Admin Configurations
# ==============================================================================

class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    Configures display fields in the list view and auto-populates slug from product name.
    """
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product Variations (color, size, etc.).
    Allows direct toggle of the active state in the list view and adds filtering.
    """
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')


# Register models to the Django Admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)