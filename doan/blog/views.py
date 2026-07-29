from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Avg
from .models import Blog, Rate, Comment

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
    comments = Comment.objects.filter(id_blog = id)
    
    # Average Rating Per Blog
    avg_rate = Rate.objects.filter(id_blog = id).aggregate(avg_rate=Avg('rate'))['avg_rate'] or 0
    
    # Pagnition
    previous_blog = Blog.objects.filter(id__lt = id).order_by('-id').first()
    next_blog = Blog.objects.filter(id__gt = id).order_by('id').first()
    
    # Render Rating Star
    stars = [1,2,3,4,5]
    rate = Rate.objects.filter(id_blog=id, id_user=request.user.id).first()
    if rate:
        user_rate = rate.rate
    else:
        user_rate = 0
    return render(request, 'blog_detail.html', {
        'blog_detail': blog_detail,
        'previous_blog': previous_blog,
        'next_blog': next_blog, 
        'comments': comments,
        'avg_rate': avg_rate,
        'stars': stars,
        'user_rate': user_rate
    })
    
# ----------------- BLOG RATING -----------------
def blog_rating_view(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        rate = request.POST.get('rate')
        try:
            if Rate.objects.filter(
                id_blog = blog_id,
                id_user = request.user.id).exists():
                return JsonResponse({'success': False, 'error': 'Only one rating allowed'})
            blog_detail = Blog.objects.get(id = blog_id)
            Rate.objects.create(
                rate = rate, 
                id_blog_id = blog_id, 
                id_user_id = request.user.id)
            return JsonResponse({'success': True})
        except Blog.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Blog not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
    
# ----------------- BLOG COMMENT -----------------
def blog_comment_view(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        comment = request.POST.get('comment')
        level = request.POST.get('level') or 0
        try:
            Blog.objects.get(id=blog_id)
            comment = Comment.objects.create(
                comment = comment,
                id_blog_id = blog_id,
                id_user_id = request.user.id,
                user_name = request.user.username,
                level = int(level)
            )
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'comment': comment.comment,
                'user_name': comment.user_name,
                'avatar': request.user.avatar.url,
                'hour': comment.created_at.strftime("%H:%M"),
                'time': comment.created_at.strftime("%d%m%Y")
            })
        except Blog.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Blog not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})