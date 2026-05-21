from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from .models import User, Contact


class SecurePasswordInput(forms.PasswordInput):
    def __init__(self, *args, **kwargs):
        kwargs['render_value'] = False
        super().__init__(*args, **kwargs)
    
    def get_context(self, name, value, attrs):
        
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
            'placeholder': 'First Name',
            'autofocus': True
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
        fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    
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
        if not email:
            return email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        
        
        if not phone.isdigit():
             raise forms.ValidationError('Only digits allowed.')

        
        if len(phone) < 10:
             raise forms.ValidationError('Minimum 10 digits required.')

        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Phone already registered.')
        return phone
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            return username
        
        
        if len(username) < 4:
            raise forms.ValidationError('Minimum 4 characters required.')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken.')
            
        
        if not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError('Only letters, numbers, and @/./+/-/_ allowed.')
            
        return username
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not password:
            return password
        
        
        if len(password) < 8:
            raise forms.ValidationError('Minimum 8 characters required.')
        
        
        if password.isdigit():
            raise forms.ValidationError('Cannot be entirely numeric.')
        
        
        common_passwords = [
            'password', '12345678', 'password123', 'qwerty', 'abc123',
            '11111111', '00000000', 'password1', '123456789', 'iloveyou'
        ]
        if password.lower() in common_passwords:
            raise forms.ValidationError('Password too common.')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        
        if password1:
            password_lower = password1.lower()
            
            if username and username.lower() in password_lower:
                self.add_error('password1', 'Too similar to username.')
            
            if email and email.split('@')[0].lower() in password_lower:
                self.add_error('password1', 'Too similar to email.')
            
            if first_name and len(first_name) > 2 and first_name.lower() in password_lower:
                self.add_error('password1', 'Too similar to first name.')
            
            if last_name and len(last_name) > 2 and last_name.lower() in password_lower:
                self.add_error('password1', 'Too similar to last name.')
        
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')
        
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


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )


class VerifyResetCodeForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        })
    )
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit code',
            'style': 'letter-spacing: 4px; font-size: 1.4rem; font-weight: 700;'
        })
    )


class VerifyEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit verification code',
            'style': 'letter-spacing: 4px; font-size: 1.4rem; font-weight: 700;'
        })
    )


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=SecurePasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=SecurePasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data




class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Current Password",
        widget=SecurePasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Current Password'
        })
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=SecurePasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=SecurePasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
        }

