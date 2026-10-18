from django.db import models
from category.models import Category
from django.urls import reverse

# ==============================================================================
# Product Catalog Models
# ==============================================================================

class Product(models.Model):
    """
    Represents an item available in the store catalog.
    Includes inventory tracking, pricing, categorization, and URL routing.
    """
    product_name = models.CharField(max_length=200, unique=True)
    slug         = models.SlugField(max_length=200, unique=True)
    description  = models.TextField(max_length=500, blank=True)
    price        = models.IntegerField()
    images       = models.ImageField(upload_to='photos/products')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)

    def get_url(self):
        """
        Generate the canonical URL for the product detail view using category and product slugs.
        """
        return reverse('products_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    """
    Custom manager for Variation model to filter variations conveniently by category.
    """
    def colors(self):
        """Return all active color variations."""
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        """Return all active size variations."""
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


# Choices for variation categories supported by products
variation_category_choice = [
    ('color', 'color'),
    ('size', 'size'),
]

class Variation(models.Model):
    """
    Represents a specific attribute/option of a product (e.g., Color, Size).
    Allows customers to pick specific variants when adding an item to the cart.
    """
    product            = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default=True)
    created_date       = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return f"{self.product.product_name} - {self.variation_category} - {self.variation_value}"