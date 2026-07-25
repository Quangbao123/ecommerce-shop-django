from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Blog, Rate

# Create your views here.
# ----------------- BLOG LIST -----------------
def blog_list_view(request):
    blog_list = Blog.objects.all().order_by('created_at')
    pagnitor = Paginator(blog_list, 3)
    page_number = request.GET.get('page')
    page_obj = pagnitor.get_page(page_number)
    return render(request, 'blog.html', {
        'page_obj': page_obj,
        'pagnitor': pagnitor
    })

# ----------------- BLOG DETAIL -----------------
def blog_detail_view(request, id):
    blog_detail = Blog.objects.get(id = id)
    previous_blog = Blog.objects.filter(id__lt = id).order_by('-id').first()
    next_blog = Blog.objects.filter(id__gt = id).order_by('id').first()
    return render(request, 'blog_detail.html', {
        'blog_detail': blog_detail,
        'previous_blog': previous_blog,
        'next_blog': next_blog
    })
    
# ----------------- BLOG RATING -----------------
def blog_rating_view(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        rate = request.POST.get('rate')
        try:
            blog_detail = Blog.objects.get(id = blog_id)
            Rate.objects.create(
                rate = rate, 
                id_blog_id = blog_id, 
                id_user_id = request.user.id)
            return JsonResponse({'success': True})
        except Blog.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Blog not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
        