from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    field_order = [
        'username', 
        'email', 
        'password', 
        'confirm_password', 
        'avatar', 
        'first_name', 
        'last_name', 
        'id_country'
    ]
    
    class Meta():
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'first_name', 'last_name', 'id_country']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'avatar': 'Avatar',
            'first_name': 'First name',
            'last_name': 'Last name',
            'id_country': 'Id country'
        }
        
    # username validation
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username = username).exists():
            raise ValidationError('Username existed')
        return username
    
    # email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email = email).exists():
            raise ValidationError('Email existed')
        return email
    
    # avatar validation
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 1024 * 1024:
                raise ValidationError('File must be smaller than 1MB')
            if not avatar.name.lower().endswitch(('.png', '.jpeg', '.jpg')):
                raise ValidationError('File extension must have jpg, jpeg or png')
        return avatar

    # consistency validation
    def clean(self):
        self.cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
