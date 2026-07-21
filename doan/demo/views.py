from django.shortcuts import render

# Create your views here.
# ----------------- HOME -----------------
def home_view(request):
    return render(request, 'base.html')