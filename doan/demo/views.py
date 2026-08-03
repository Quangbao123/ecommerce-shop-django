from django.shortcuts import render
from product.models import Product
import json
# Create your views here.
# ----------------- HOME -----------------
def home_view(request):
    products = Product.objects.all()
    for product in products:
        product.image_filenames = json.loads(product.image)
    return render(request, 'index.html', {'products': products})
