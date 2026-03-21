from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q, Min
from django.utils import timezone
from datetime import timedelta
import random

from .models import User, Contact
from products.models import Order
from appointments.models import Appointment
from .forms import (
    UserRegistrationForm, UserLoginForm, ForgotPasswordForm, 
    VerifyResetCodeForm, ResetPasswordForm, ChangePasswordForm,
    UserProfileForm
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
    from django.utils import timezone
    from appointments.models import Appointment
    from products.models import Sale
    from accounts.models import Contact

    # 1. Total Users (Blue)
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()

    # 2. Total Bookings (Green)
    total_bookings = Appointment.objects.count()
    today_bookings = Appointment.objects.filter(appointment_date=timezone.now().date()).count()

    # 3. Tasks Completion (Cyan ProgressBar)
    completed_appointments = Appointment.objects.filter(status='completed').count()
    tasks_percentage = 0
    if total_bookings > 0:
        tasks_percentage = int((completed_appointments / total_bookings) * 100)

    # 4. Pending Appointments (Orange)
    pending_appointments = Appointment.objects.filter(status='pending').count()

    # History Data
    recent_appointments = Appointment.objects.select_related('user').all().order_by('-created_at')[:5]
    from products.models import Product
    low_stock_products = Product.objects.filter(stock_quantity__lt=10).order_by('stock_quantity')[:5]

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_bookings': total_bookings,
        'today_bookings': today_bookings,
        'tasks_percentage': tasks_percentage,
        'pending_appointments': pending_appointments,
        'recent_appointments': recent_appointments,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)

    # Fetch user stats for the profile page
    total_appointments = Appointment.objects.filter(user=request.user).count()
    total_orders = Order.objects.filter(user=request.user).count()
    # Assume 1 order item = 1 point for now as a simple loyalty placeholder
    member_points = total_orders * 10 
    
    context = {
        'form': form,
        'total_appointments': total_appointments,
        'total_orders': total_orders,
        'member_points': member_points,
    }
    return render(request, 'accounts/user_profile.html', context)


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
    from products.models import Sale
    from django.db.models import Sum
    import calendar
    from datetime import datetime

    # Get filter parameters
    now = datetime.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))

    # Get all sales for filtering
    all_sales = Sale.objects.all()

    # Monthly Stats
    monthly_sales = all_sales.filter(
        sale_date__month=selected_month,
        sale_date__year=selected_year
    )
    monthly_revenue = monthly_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    monthly_sales_count = monthly_sales.count()

    # Yearly Stats
    yearly_sales = all_sales.filter(sale_date__year=selected_year)
    yearly_revenue = yearly_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    yearly_sales_count = yearly_sales.count()

    # Sales list for the selected month/year with pagination
    sales_list = monthly_sales.order_by('-sale_date')
    paginator = Paginator(sales_list, 10)
    page_number = request.GET.get('page')
    sales_page = paginator.get_page(page_number)

    # Context data for filters
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
    # Get range of years from sales or at least last 5 years
    min_year = all_sales.aggregate(Min('sale_date'))['sale_date__min']
    if min_year:
        start_year = min_year.year
    else:
        start_year = now.year - 4
    
    years = range(start_year, now.year + 1)

    context = {
        'months': months,
        'years': years,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'monthly_revenue': monthly_revenue,
        'monthly_sales_count': monthly_sales_count,
        'yearly_revenue': yearly_revenue,
        'yearly_sales_count': yearly_sales_count,
        'sales_page': sales_page,
    }
    return render(request, 'accounts/reports.html', context)


@login_required
@admin_required
def export_sales_csv(request):
    import csv
    from django.http import HttpResponse
    from products.models import Sale
    from datetime import datetime
    import calendar

    # Get filter parameters
    now = datetime.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))

    # Filename
    month_name = calendar.month_name[selected_month]
    filename = f"Sales_Report_{month_name}_{selected_year}.csv"

    # Create response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Sale ID', 'Product', 'Customer', 'Quantity', 'Unit Price', 'Total Amount', 'Payment Method', 'Date'])

    # Get data
    sales = Sale.objects.filter(
        sale_date__month=selected_month,
        sale_date__year=selected_year
    ).order_by('-sale_date')

    for sale in sales:
        customer_name = sale.customer.get_full_name() or sale.customer.username if sale.customer else "Walk-in"
        writer.writerow([
            sale.id,
            sale.product.name,
            customer_name,
            sale.quantity,
            sale.unit_price,
            sale.total_amount,
            sale.get_payment_method_display(),
            sale.sale_date.strftime('%Y-%m-%d %H:%M')
        ])

    return response


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
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to send a message.')
            return redirect('login')
            
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact_us')
    
    faqs = [
        {
            'question': 'What are your opening hours?',
            'answer': 'We are open Sunday through Friday, from 10:00 AM to 6:00 PM. We are closed on Saturdays and public holidays.'
        },
        {
            'question': 'Do I need to book an appointment in advance?',
            'answer': 'Yes, we highly recommend booking an appointment to ensure your pet gets the dedicated time they deserve. You can book directly through our website or call us.'
        },
        {
            'question': 'How long does a typical grooming session take?',
            'answer': 'A standard grooming session usually takes between 2 to 4 hours, depending on the breed, coat condition, and services requested.'
        },
        {
            'question': 'Do you groom all breeds of dogs and cats?',
            'answer': 'Yes, we welcome all breeds and sizes of both dogs and cats! Our groomers are experienced with various coat types and temperaments.'
        },
        {
            'question': 'What vaccinations are required for grooming?',
            'answer': 'For the safety of all our furry guests, we require pets to be up-to-date on their rabies vaccination and recommend being current on other core vaccines.'
        }
    ]
        
    return render(request, 'contact.html', {'faqs': faqs})


@login_required
def my_contact_requests(request):
    messages_list = Contact.objects.filter(email=request.user.email).order_by('-id')
    
    return render(request, 'accounts/my_contact_request.html', {
        'messages_list': messages_list
    })
