from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
import random

from .models import User, Contact
from products.models import Order
from appointments.models import Appointment
from .forms import (
    UserRegistrationForm, UserLoginForm, ForgotPasswordForm, 
    VerifyResetCodeForm, ResetPasswordForm, ChangePasswordForm
)
from .decorators import admin_required


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate a 6-digit code
                code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                user.reset_code = code
                user.reset_code_expires_at = timezone.now() + timedelta(minutes=15)
                user.save()
                
                # Store email in session for verification
                request.session['reset_email'] = email
                
                # Debug print for console
                print(f"DEBUG: Password reset code for {email} is {code}")
                
                # Attempt to send actual email
                try:
                    send_mail(
                        'Password Reset - Himalayan Pet Studio',
                        f'Your verification code is: {code}\n\nThis code expires in 15 minutes.',
                        None,  # Uses DEFAULT_FROM_EMAIL from settings
                        [email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Error sending email: {e}")
                    messages.warning(request, f"Email failed to send: {str(e)}. However, you can check the server console for the code.")
                
                messages.success(request, f"A reset code has been sent to {email}.")
                return redirect('verify_reset_code')
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})


def verify_reset_code(request):
    if request.method == 'POST':
        form = VerifyResetCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(email=email, reset_code=code)
                if user.reset_code_expires_at > timezone.now():
                    # Valid code, store email in session for the reset page
                    request.session['reset_email'] = email
                    return redirect('reset_password')
                else:
                    messages.error(request, "Reset code has expired.")
            except User.DoesNotExist:
                messages.error(request, "Invalid email or reset code.")
    else:
        form = VerifyResetCodeForm()
    return render(request, 'accounts/verify_reset_code.html', {'form': form})


def reset_password(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=email)
                user.set_password(form.cleaned_data['new_password1'])
                user.reset_code = None
                user.reset_code_expires_at = None
                user.save()
                
                # Clear session
                del request.session['reset_email']
                
                messages.success(request, "Password has been reset successfully. Please login.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "Something went wrong. Please try again.")
    else:
        form = ResetPasswordForm()
    return render(request, 'accounts/reset_password.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                # We need to re-login the user or they will be logged out
                login(request, user)
                messages.success(request, "Your password has been changed successfully.")
                return redirect('user_profile')
            else:
                form.add_error('old_password', 'Current password is incorrect.')
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/change_password.html', {'form': form})


def home(request):
    if request.user.is_authenticated and request.user.is_admin_user():
        return redirect('admin_dashboard')
    
    # Get active services from DB
    from appointments.models import Service, ServiceReview
    from django.db.models import Avg, Count
    
    services = Service.objects.filter(is_active=True).order_by('order')
    
    # Get service ratings for backward compatibility / specific needs
    service_ratings = {}
    for svc in services:
        reviews = ServiceReview.objects.filter(service=svc.slug)
        avg = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        count = reviews.count()
        svc.avg_rating = round(avg, 1) if avg else 0
        svc.review_count = count
        service_ratings[svc.slug] = {
            'avg_rating': svc.avg_rating,
            'review_count': count
        }
    
    # Get top rated products
    from products.models import Product
    top_rated_products = Product.objects.filter(
        is_active=True,
        stock_quantity__gt=0
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0
    ).order_by('-avg_rating')[:8]
    
    # Get top selling products (most orders)
    from products.models import OrderItem
    top_products = Product.objects.filter(
        is_active=True,
        stock_quantity__gt=0
    ).annotate(
        total_sold=Count('orderitem')
    ).filter(
        total_sold__gt=0
    ).order_by('-total_sold')[:5]
    
    context = {
        'services': services,
        'service_ratings': service_ratings,
        'top_rated_products': top_rated_products,
        'top_products': top_products,
    }
    
    return render(request, 'home.html', context) 


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user():
            return redirect('admin_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user and user.is_active:
                login(request, user)
                messages.success(request, 'Login successful')

                if user.is_admin_user():
                    return redirect('admin_dashboard')
                return redirect('home')
            else:
                # Add error to form instead of using messages
                form.add_error(None, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.is_active = True
            user.save()

            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
@admin_required
def admin_dashboard(request):
    # Calculate Earnings (Paid Orders)
    total_earnings = Order.objects.filter(
        Q(payment_status='paid') | Q(status='completed')
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Pending Requests (Pending Appointments + Unread Messages)
    pending_appointments = Appointment.objects.filter(status='pending').count()
    unread_messages = Contact.objects.filter(is_read=False).count()
    pending_requests = pending_appointments + unread_messages

    # Tasks Progress (Completed vs Total Appointments)
    total_appointments = Appointment.objects.count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    
    if total_appointments > 0:
        tasks_percentage = int((completed_appointments / total_appointments) * 100)
    else:
        tasks_percentage = 0

    context = {
        'total_earnings': total_earnings,
        'annual_earnings': total_earnings, # For now, same as total. Can filter by year later.
        'pending_requests': pending_requests,
        'tasks_percentage': tasks_percentage,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')


@login_required
def user_profile(request):
    return render(request, 'accounts/user_dashboard.html') # Placeholder: reusing dashboard template for now


@login_required
@admin_required
def user_list(request):
    users_list = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users_list, 10)  # Show 10 users per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/user_list.html', {
        'users': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })


@login_required
@admin_required
def user_detail(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    return render(request, 'accounts/user_detail.html', {'user_obj': user_obj})


@login_required
@admin_required
def reports(request):
    return render(request, 'accounts/reports.html')


@login_required
@admin_required
def contact_messages(request):
    messages_list = Contact.objects.all().order_by('-created_at')
    paginator = Paginator(messages_list, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check for unread messages count for the sidebar badge
    unread_count = Contact.objects.filter(is_read=False).count()
    
    return render(request, 'accounts/contact_messages.html', {
        'messages': page_obj,
        'page_obj': page_obj, 
        'is_paginated': page_obj.has_other_pages(),
        'unread_count': unread_count
    })


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact_us')
        
    return render(request, 'contact.html')



