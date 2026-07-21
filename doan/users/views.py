from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
# ----------------- REGISTER -----------------
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) # 
            
            # Permissions
            user.is_superuser = False
            user.is_staff = True
            
            user.save()
            # return HttpResponse('Register successfully, sent email')
            return redirect('user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# ----------------- LOGIN -----------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            request.session['user_id'] = user.id
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# ----------------- LOGOUT -----------------
def custom_logout(request):
    logout(request)
    return redirect('user_login')