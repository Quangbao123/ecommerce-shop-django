from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm
# Create your views here.

# ----------------- HOME -----------------
def home_view(request):
    return render(request, 'base.html')

# ----------------- REGISTER -----------------
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) # 
            
            # Permissions
            user.is_superuser = False
            user.is_staff = True
            
            user.save()
            return HttpResponse('Register successfully, sent email')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})