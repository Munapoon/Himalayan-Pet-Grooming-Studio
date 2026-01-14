from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from .models import User, Contact


# Custom password widget that NEVER renders values
class SecurePasswordInput(forms.PasswordInput):
    def __init__(self, *args, **kwargs):
        kwargs['render_value'] = False
        super().__init__(*args, **kwargs)
    
    def get_context(self, name, value, attrs):
        # Always set value to None to prevent rendering
        return super().get_context(name, None, attrs)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget = SecurePasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'id_password1',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget = SecurePasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'id': 'id_password2',
            'autocomplete': 'new-password'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Check if phone contains only digits
        if not phone.isdigit():
             raise forms.ValidationError('Phone number must contain only digits.')

        # Check minimum length (e.g. at least 10 digits)
        if len(phone) < 10:
             raise forms.ValidationError('Phone number must be at least 10 digits long.')

        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('This phone number is already registered.')
        return phone
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Check minimum length
        if len(username) < 4:
            raise forms.ValidationError('Username must be at least 4 characters long.')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
            
        # Check for valid characters
        if not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError('Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.')
            
        return username
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Check minimum length
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        
        # Check if entirely numeric
        if password.isdigit():
            raise forms.ValidationError('Password cannot be entirely numeric.')
        
        # Check for common passwords
        common_passwords = [
            'password', '12345678', 'password123', 'qwerty', 'abc123',
            '11111111', '00000000', 'password1', '123456789', 'iloveyou'
        ]
        if password.lower() in common_passwords:
            raise forms.ValidationError('This password is too common. Please choose a more secure password.')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        # Check if password is too similar to personal information
        if password1:
            password_lower = password1.lower()
            
            if username and username.lower() in password_lower:
                self.add_error('password1', 'Password is too similar to your username.')
            
            if email and email.split('@')[0].lower() in password_lower:
                self.add_error('password1', 'Password is too similar to your email address.')
            
            if first_name and len(first_name) > 2 and first_name.lower() in password_lower:
                self.add_error('password1', 'Password is too similar to your first name.')
            
            if last_name and len(last_name) > 2 and last_name.lower() in password_lower:
                self.add_error('password1', 'Password is too similar to your last name.')
        
        # Check if passwords match
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'The two password fields must match.')
        
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=SecurePasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'id_password',
            'autocomplete': 'off'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

