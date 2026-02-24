from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import User, Contact
from products.models import Order
from appointments.models import Appointment
from django.db.models import Sum, Q
from .forms import UserRegistrationForm, UserLoginForm
from .decorators import admin_required


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



