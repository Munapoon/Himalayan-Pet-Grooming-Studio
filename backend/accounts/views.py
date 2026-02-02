from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm
from .decorators import admin_required


def home(request):
    if request.user.is_authenticated and request.user.is_admin_user():
        return redirect('admin_dashboard')
    
    # Get service ratings
    from appointments.models import ServiceReview
    from django.db.models import Avg, Count
    
    service_types = ['bath', 'full', 'haircut', 'nails']
    service_ratings = {}
    
    for service_type in service_types:
        reviews = ServiceReview.objects.filter(service=service_type)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        review_count = reviews.count()
        service_ratings[service_type] = {
            'avg_rating': round(avg_rating, 1) if avg_rating else 0,
            'review_count': review_count
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
    return render(request, 'accounts/admin_dashboard.html')


@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')


@login_required
def user_profile(request):
    return render(request, 'accounts/user_dashboard.html') # Placeholder: reusing dashboard template for now
