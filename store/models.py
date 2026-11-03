from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count

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

    
    def averageReview(self):
        """
        Calculate the average rating for this product based on approved reviews.
        Returns 0 if there are no reviews.
        """
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg


    def countReviews(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count=int(reviews['count'])
        return count

    def countReview(self):
        return self.countReviews()
    

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
        return self.variation_value


class ReviewRating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=500,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'