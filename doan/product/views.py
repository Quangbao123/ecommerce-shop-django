from django.shortcuts import render
from .models import Brand, Category, Product
from django.conf import settings
import os, json
from django.http import JsonResponse
from PIL import Image

# Create your views here.
# ----------------- CREATE PRODUCT -----------------
def add_product_view(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        status = int(request.POST.get('status'))
        sale = request.POST.get('sale')
        company = request.POST.get('company')
        files = request.FILES.getlist('image')
        detail = request.POST.get('detail')
        
        errors = {}
        # validate product name
        if not name:
            errors['name'] = 'Product Name Required'
        # validate price
        if not price:
            errors['price'] = 'Product Price Required'
        else:
            try:
                price = float(price)
                if price < 0:
                    errors['price'] = 'Price must be postive'
            except ValueError:
                errors['price'] = 'Price must be a number'
        
        # validate category
        if not category:
            errors['category'] = 'Category Required'
        # validate brand
        if not brand:
            errors['brand'] = 'Brand Required'
        # validate sale
        if status == 1 and not sale:
            errors['sale'] = 'Sale Required'
        # validate company profile
        if not company:
            errors['company'] = 'Company Required'
        # validate files
        if not files:
            errors['images'] = 'Choose at least 1 image'
        elif len(files) > 3:
            errors['images'] = 'Only upload maximum of 3 images'
        else:
            for file in files:
                if file.content_type not in ['image/jpeg', 'image/png']:
                    errors['images'] = f"{file.name} is not a valid image"
                    break
                if file.size > 1 * 1024 * 1024:
                    errors['images'] = f"{file.name} exceeds 1 MB"
                    break
        # validate detail
        if not detail:
            errors['detail'] = 'Detail Required'
        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
        
        saved_filenames = []
        for file in files:
            filename = file.name.replace(" ", "_")
            base, ext = os.path.splitext(filename)
            ext = ext.lower()
            save_folder = os.path.join(settings.MEDIA_ROOT, 'products')
            os.makedirs(save_folder, exist_ok=True)
            original_path = os.path.join(save_folder, f"{base}{ext}")
            with open(original_path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
                    
            saved_filenames.append(f"{base}{ext}")
            img = Image.open(original_path)
            for size in [100,200]:
                img_copy = img.copy()
                img_copy.thumbnail((size, size))
                resized_name = f"{size}_{base}{ext}"
                resized_path = os.path.join(save_folder, resized_name)
                img_copy.save(resized_path)
        
        Product.objects.create(
            id_user_id = request.user.id,
            name=name,
            price=price,
            id_category_id = category,
            id_brand_id = brand,
            status=status,
            sale=int(sale) if sale else 0,
            company=company,
            image=json.dumps(saved_filenames),
            detail=detail
        )
        return JsonResponse({'success': True, 'status': 'success'})
    return render(request, 'addProduct.html', {
        'brands': brands,
        'categories': categories,
        'account_page': True
    })
    
# ----------------- DISPLAY PRODUCT -----------------
def display_product_view(request):
    products = Product.objects.filter(id_user_id=request.user.id)
    for product in products:
        product.image_filenames = json.loads(product.image)
    return render(request, 'myProduct.html', {
        'products': products,
        'account_page': True
    })