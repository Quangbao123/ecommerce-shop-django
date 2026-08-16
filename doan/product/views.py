from django.shortcuts import render
from .models import Brand, Category, Product
from django.conf import settings
from django.template.loader import render_to_string
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
        if product.status == 1 and product.sale > 0:
            product.final_price = product.price * (100 - product.sale)/100
        else:
            product.final_price = product.price
    return render(request, 'myProduct.html', {
        'products': products,
        'account_page': True
    })

# ----------------- EDIT PRODUCT -----------------
def edit_product_view(request, id):
    product = Product.objects.get(id=id)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    product.image_filenames = json.loads(product.image)
    current_images = product.image_filenames
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        status = int(request.POST.get('status'))
        sale = request.POST.get('sale')
        company = request.POST.get('company')
        new_files = request.FILES.getlist('image')
        detail = request.POST.get('detail')
        
        images_delete = request.POST.getlist('hinhxoa[]')
        
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
        rest_images = [img for img in current_images if img not in images_delete]
        if new_files:
            for file in new_files:
                if file.content_type not in ['image/jpeg', 'image/png']:
                    errors['images'] = f"{file.name} is not a valid image"
                    break
                if file.size > 1 * 1024 * 1024:
                    errors['images'] = f"{file.name} exceeds 1 MB"
                    break
            if len(new_files) + len(rest_images) > 3:
                errors['images'] = 'Total images cannot exceeds 3'
                
        # validate detail
        if not detail:
            errors['detail'] = 'Detail Required'
        if errors:
            return JsonResponse({ 'success': False, 'errors': errors }, status=400)
        
        saved_new_filenames = []
        save_folder = os.path.join(settings.MEDIA_ROOT, 'products')
        # Delete old images
        for img_name in images_delete:
            file_path = os.path.join(save_folder, img_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            for size in [100,200]:
                thumb_path = os.path.join(save_folder, f'{size}_{img_name}')
                if os.path.exists(thumb_path):
                    os.remove(thumb_path)
        if new_files:
            for file in new_files:
                os.makedirs(save_folder, exist_ok=True)
                for file in new_files:
                    filename = file.name.replace(' ', '_')
                    base, ext = os.path.splitext(filename)
                    ext = ext.lower()
                    
                    original_path = os.path.join(save_folder, f"{base}{ext}")
                    with open(original_path, 'wb+') as dest:
                        for chunk in file.chunks():
                            dest.write(chunk)
                                        
                    saved_new_filenames.append(f"{base}{ext}")
                    img = Image.open(original_path)
                    for size in [100,200]:
                        img_copy = img.copy()
                        img_copy.thumbnail((size, size))
                        resized_name = f"{size}_{base}{ext}"
                        resized_path = os.path.join(save_folder, resized_name)
                        img_copy.save(resized_path)
        final_image_arr = saved_new_filenames + rest_images
        
        product.name = name
        product.price = float(price)
        product.id_category_id = category
        product.id_brand_id = brand
        product.status = status
        product.sale = int(sale) if sale and status == 1 else 0
        product.company = company
        product.detail = detail
        product.image = json.dumps(final_image_arr) # => json => database
        product.save()
        return JsonResponse({'success': True, 'status': 'success'})
    
    return render(request, 'editProduct.html', {
        'product': product,
        'brands': brands,
        'categories': categories,
        'account_page': True
    })

# ----------------- DELETE PRODUCT -----------------
def delete_product_view(request, id):
    if request.method == "POST":
        product = Product.objects.get(id=id)
        images = json.loads(product.image)
        for img in images:
            file_path = os.path.join(settings.MEDIA_ROOT, 'products', img)
            if os.path.exists(file_path):
                os.remove(file_path)
        product.delete()
        return JsonResponse({'success': True, 'status': 'success'})
    return JsonResponse({'success': False, 'status': 'error', 'message': 'Invalid Request'}, status=400)


# ----------------- PRODUCT DETAIL -----------------
def product_detail_view(request, id):
    product = Product.objects.get(id=id)
    product.image_filenames = json.loads(product.image)
    sale = 1 if product.status == 0 else (100 - product.sale)/100
    product.final_price = product.price * sale
    return render(request, 'productDetail.html', {
        'product': product
    })
    
# ----------------- SEARCH PRODUCT -----------------
def search_view(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    for product in products:
        product.image_filenames = json.loads(product.image)
        if product.status == 1 and product.sale > 0:
            product.final_price = product.price * (100 - product.sale)/100
        else:
            product.final_price = product.price
    return render(request, 'productList.html', {
        'products': products
    })

def searchAjax_view(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
            
    name = request.GET.get('name', '').strip()
    price = request.GET.get('price', '').strip()
    category = request.GET.get('category', '')
    brand = request.GET.get('brand', '')
    status = request.GET.get('status', '')
    
    if name:
        products = products.filter(name__icontains=name)
        
    if category:
        products = products.filter(id_category_id=category)
        
    if brand:
        products = products.filter(id_brand_id=brand)
    
    if status != '' and status is not None:
        products = products.filter(status=status)
        
    product_list = []
    for product in products:
        product.image_filenames = json.loads(product.image)

        if str(product.status) == '1' and product.sale > 0:
            product.final_price = product.price * (100 - product.sale)/100
        else:
            product.final_price = product.price
            
        if price:
            min_p, max_p = map(int, price.split('-'))
            if not (min_p <= product.final_price <= max_p):
                continue
        product_list.append(product)
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        html = render_to_string('product_list_ajax.html', {'products': product_list}, request=request)
        return JsonResponse({'html': html})
    
    return render(request, 'searchAjax.html', {
        'brands': brands,
        'categories': categories,
        'products': product_list
    })

def searchReload_view(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    
    name = request.GET.get('name', '').strip()
    price = request.GET.get('price', '').strip()
    category = request.GET.get('category', '')
    brand = request.GET.get('brand', '')
    status = request.GET.get('status', '')
    
    if name:
        products = products.filter(name__icontains=name)
        
    if category:
        products = products.filter(id_category_id=category)
        
    if brand:
        products = products.filter(id_brand_id=brand)
    
    if status != '' and status is not None:
        products = products.filter(status=status)
        
    product_list = []
    for product in products:
        product.image_filenames = json.loads(product.image)
        if str(product.status) == '1' and product.sale > 0:
            product.final_price = product.price * (100 - product.sale)/100
        else:
            product.final_price = product.price
            
        if price:
            min_p, max_p = map(int, price.split('-'))
            if not (min_p <= product.final_price <= max_p):
                continue
        product_list.append(product)
    
    return render(request, 'searchReload.html', {
        'brands': brands,
        'categories': categories,
        'products': product_list
    })