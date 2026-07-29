from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .models import Country
from django.core.exceptions import ValidationError

# Create your views here.
# ----------------- REGISTER -----------------
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            
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

# ----------------- USER ACCOUNT UPDATE -----------------
def update_account_view(request):
    user = request.user
    countries = Country.objects.all()
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        
        if password:
            user.set_password(password)
            update_session_auth_hash(request,user)
        user.id_country_id = request.POST.get('country')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        avatar = request.FILES.get('avatar')
        if avatar:
            if avatar.size > 1024 * 1024:
                return render(request, 'accountUpdate.html', {
                    'user_info': user,
                    'countries': countries,
                    'error': 'Avatar must be smaller than 1MB.'
                })
            if not avatar.name.lower().endswith(('.png', '.jpeg', '.jpg')):
                return render(request, 'accountUpdate.html', {
                    'user_info': user,
                    'countries': countries,
                    'error': 'Avatar must be JPG, JPEG or PNG.'
                })
            user.avatar = request.FILES.get('avatar')
        user.save()
        return redirect('account_update')
        
    return render(request, 'accountUpdate.html', {
        "user_info": user,
        "countries": countries,
        "account_page": True
    })
            