from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# ==============================================================================
# Shopping Cart Models
# ==============================================================================

class Cart(models.Model):
    """
    Represents a shopping cart instance.
    Uses a unique session key (cart_id) to associate carts with guest/browser sessions.
    """
    cart_id    = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class Cartitem(models.Model):
    """
    Represents an individual product item placed inside a Cart.
    Tracks selected product variations (color, size), quantity, and active state.
    """
    user       = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, null=True)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart       = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity   = models.IntegerField()
    is_active  = models.BooleanField(default=True)

    def sub_total(self):
        """
        Calculate total price for this line item based on unit price and quantity.
        """
        return self.product.price * self.quantity
    
    def __str__(self):
        return str(self.product)
