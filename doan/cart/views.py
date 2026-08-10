from django.shortcuts import render, redirect
from product.models import Product
from django.http import JsonResponse
from users.forms import UserRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from .models import History
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
            'status': 'success',
            'cart_count': cart_count(cart)
        })

# ----------------- VIEW PRODUCT CART -----------------
def view_product_cart(request):
    cart = request.session.get('cart', {})
    for product in cart.values():
        product['total_price'] = (
            product['quantity'] * product['price']
        )
    return render(request, 'cart.html', {
        'no_left': True
    })
    
# ----------------- UPDATE CART -----------------
def update_cart_view(request, id):
    cart = request.session.get('cart', {})
    action = request.POST.get('action')
    if str(id) not in cart:
        return JsonResponse({
            'success': False,
            'message': 'Product not found'
        })
    product = cart[str(id)]
    if action == 'up':
        product['quantity'] += 1
    elif action == 'down':
        if product['quantity'] > 1:
            product['quantity'] -= 1
    request.session['cart'] = cart
    request.session.modified = True
    total = product['quantity'] * product['price']
    return JsonResponse({
        'success': True,
        'quantity': product['quantity'],
        'total': total,
        'cart_count': cart_count(cart)
    })

# ----------------- DELETE CART -----------------
def delete_product_cart_view(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
        request.session['cart'] = cart
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': 'Product deleted',
            'cart_count': cart_count(cart)
        })
    return JsonResponse({
        'success': False,
        'message': 'Product not found',
    })

def cart_count(cart):
    return sum(item['quantity'] for item in cart.values())

# ----------------- DISPLAY CHECKOUT -----------------
def checkout_view(request):
    cart = request.session.get('cart', {})
    for product in cart.values():
        product['total_price'] = (
            product['quantity'] * product['price']
        )
    
    # Register
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            # Permissions
            user.is_superuser = False
            user.is_staff = True
            user.save()
            # Send email
            send_welcome_email(user)
            
            return HttpResponse('Register successfully, sent email')
    else:
        form = UserRegisterForm()
    return render(request, 'checkout.html', {
        'no_left': True,
        'form': form
    })

# ----------------- EMAIL -----------------
def send_welcome_email(user):
    subject = 'Chào mừng bạn đến với website!'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    # Nội dung text fallback
    text_content = f"Chào {user.username}, cảm ơn bạn đã đăng ký."

    # Render HTML từ template
    html_content = render_to_string('emails/welcome_email.html',{'user': user})

    # Gửi email
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# ----------------- Order -----------------
def order_view(request):
    cart = request.session.get('cart', {})
    for product in cart.values():
        product['total_price'] = (
            product['quantity'] * product['price']
        )
    total_price = 0
    for item in cart.values():
        total_price += item['total_price']
    user = request.user
    history = History.objects.create(
        user = user,
        name = user.username,
        email = user.email,
        price = total_price
    )
    html_content = render_to_string(
        'emails/order_email.html',
        {
            'user': user,
            'cart': cart,
            'history': history,
            'total_price': total_price,
        }
    )
    text_content = (
        f"Xin chào {user.username},\n\n"
        f"Cảm ơn bạn đã đặt hàng.\n"
        f"Tổng tiền: ${total_price}"
    )
    subject = 'Xác nhận đơn hàng'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    request.session['cart'] = {}
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'message': 'Đặt hàng thành công!'
    })