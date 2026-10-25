from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, Cartitem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# ==============================================================================
# Helper Functions
# ==============================================================================

def _cart_id(request):
    """
    Retrieve or initialize the unique cart identifier using Django session keys.
    This enables cart persistence for guest visitors without requiring user authentication.
    """
    cart = request.session.session_key
    if not cart:
        # Create a new session if one does not exist for the current visitor
        request.session.create()
        cart = request.session.session_key
    return cart


# ==============================================================================
# Cart Views
# ==============================================================================

def add_cart(request, product_id):
    """
    Add a product to the user's shopping cart.
    - Captures any chosen variations (such as color and size) from POST parameters.
    - Retrieves or creates the visitor's Cart using their session ID.
    - If the product already exists in the cart, increments the quantity and updates variations.
    - If the product is not yet in the cart, creates a new Cartitem.
    - Redirects to the cart page after completion.
    """
    product = Product.objects.get(id=product_id)
    product_variation = []
    
    # Process POST data to capture product options (e.g., color, size)
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[item]
            
            try:
                # Look up matching Variation record for this product
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                # Ignore non-variation form fields (such as csrfmiddlewaretoken)
                pass

    # Retrieve or create the Cart for the current session
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    is_cart_item_exists=Cartitem.objects.filter(product=product,cart=cart).exists()
    if is_cart_item_exists:
        cart_item=Cartitem.objects.filter(product=product,cart=cart)

        ex_var_list=[]
        id=[]
        for item in cart_item:
            existing_variation=item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        print(ex_var_list)

        if product_variation in ex_var_list:
            index=ex_var_list.index(product_variation)
            item_id=id[index]
            item=Cartitem.objects.get(product=product,id=item_id)
            item.quantity+=1
            item.save()

        else:
            item=Cartitem.objects.create(product=product,quantity=1,cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        # Create new cart item entry
        cart_item = Cartitem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
        
    return redirect('cart')


def remove_cart(request, product_id,cart_item_id):
    """
    Decrement the quantity of a product in the cart.
    If the quantity drops to 1 and the user decrements again, the Cartitem is deleted.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = Cartitem.objects.get(product=product, cart=cart,id=cart_item_id)
    
        if cart_item.quantity > 1:
        # Decrement quantity by 1
            cart_item.quantity -= 1
            cart_item.save()
        else:
        # If quantity would reach 0, remove the item completely
            cart_item.delete()
    except:
        pass    
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    """
    Completely remove a product from the shopping cart regardless of its quantity.
    Triggered when the user clicks 'Remove' on the cart page.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cartitem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    """
    Render the shopping cart view.
    - Fetches all active Cartitems associated with the current session.
    - Calculates total price and item quantity.
    - Computes 2% estimated tax and grand total.
    - Handles cases where the cart does not exist gracefully.
    """
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        # Accumulate total cost and item count
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        # 2% estimated sales tax
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        # Cart does not exist yet (session is empty)
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='signin')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        # Accumulate total cost and item count
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        # 2% estimated sales tax
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        # Cart does not exist yet (session is empty)
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)