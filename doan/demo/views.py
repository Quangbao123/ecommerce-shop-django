from django.shortcuts import render
from product.models import Product
from django.http import JsonResponse
import json
# Create your views here.
# ----------------- HOME -----------------
def home_view(request):
    products = Product.objects.all()
    for product in products:
        product.image_filenames = json.loads(product.image)
    return render(request, 'index.html', {'products': products})

# ----------------- ADD PRODUCT TO CART -----------------
def add_to_cart_view(request, id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        product.image_filenames = json.loads(product.image)
        sale = 1 if product.status == 0 else (100 - product.sale)/100
        product.final_price = product.price * sale

        cart = request.session.get('cart', {})
        if str(id) in cart:
            cart[str(id)]['quantity'] += 1
        else:
            cart[str(id)] = {
                'id': product.id,
                'name': product.name,
                'image': product.image_filenames[0],
                'price': product.final_price,
                'quantity': 1,
            }
        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'status': 'success'
        })

# ----------------- VIEW PRODUCT CART -----------------
def view_product_cart(request):
    return render(request, 'cart.html', {
        'no_left': True
    })