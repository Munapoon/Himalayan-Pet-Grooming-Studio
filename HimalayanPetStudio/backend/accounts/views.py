from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .decorators import admin_required, user_required
from .models import User



def home(request):
    from appointments.forms import AppointmentForm
    from products.models import Product
    from django.db.models import Sum, Avg
    
    if request.user.is_authenticated:
        form = AppointmentForm(initial={'user': request.user})
    else:
        form = AppointmentForm()
    
    top_products = Product.objects.filter(
        is_active=True,
        sales__isnull=False
    ).annotate(
        total_sold=Sum('sales__quantity')
    ).order_by('-total_sold')[:6]
    
    top_rated_products = Product.objects.filter(
        is_active=True,
        reviews__isnull=False
    ).annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(avg_rating__gte=4.0).order_by('-avg_rating', '-created_at')[:6]
    
    context = {
        'form': form,
        'top_products': top_products,
        'top_rated_products': top_rated_products,
    }
    return render(request, 'home.html', context)


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user():
            return redirect('admin_dashboard')
        else:
            return redirect('user_dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    if remember_me:
                        request.session.set_expiry(1209600)
                    else:
                        request.session.set_expiry(0)
                    
                    request.session['user_role'] = user.role
                    request.session['user_id'] = user.id
                    request.session.modified = True
                    
                    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                    
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    elif user.is_admin_user():
                        return redirect('admin_dashboard')
                    else:
                        return redirect('user_dashboard')
                else:
                    messages.error(request, 'Your account has been disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.is_active = True
            user.save()
            
            login(request, user)
            
            request.session['user_role'] = user.role
            request.session['user_id'] = user.id
            request.session.set_expiry(86400)
            request.session.modified = True
            
            messages.success(request, f'Welcome to Himalayan Pet Studio, {user.get_full_name() or user.username}!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        request.session.flush()
        logout(request)
        messages.success(request, f'Goodbye {username}! You have been logged out successfully.')
    
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.is_admin_user():
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')


@login_required
@admin_required
def admin_dashboard(request):
    from appointments.models import Appointment
    from products.models import Product, ProductCategory, Order
    from django.db.models import Count, Sum
    from datetime import date, timedelta
    from django.utils import timezone
    
    total_users = User.objects.filter(role='user').count()
    active_users = User.objects.filter(role='user', is_active=True).count()
    
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    today_appointments = Appointment.objects.filter(appointment_date=date.today()).count()
    
    total_products = Product.objects.count()
    total_categories = ProductCategory.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    out_of_stock = Product.objects.filter(stock_quantity=0).count()
    
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_revenue = Order.objects.filter(payment_status='pending').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    total_inventory_value = Product.objects.aggregate(total=Sum('price'))['total'] or 0
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    monthly_appointments = Appointment.objects.filter(created_at__gte=thirty_days_ago).count()
    
    current_year = timezone.now().year
    yearly_appointments = Appointment.objects.filter(created_at__year=current_year).count()
    
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:10]
    recent_orders = Order.objects.all().select_related('user').prefetch_related('items').order_by('-created_at')[:10]
    low_stock_products = Product.objects.filter(stock_quantity__lte=5, stock_quantity__gt=0, is_active=True).order_by('stock_quantity')[:5]
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'today_appointments': today_appointments,
        'total_products': total_products,
        'total_categories': total_categories,
        'active_products': active_products,
        'out_of_stock': out_of_stock,
        'total_inventory_value': total_inventory_value,
        'monthly_appointments': monthly_appointments,
        'yearly_appointments': yearly_appointments,
        'recent_appointments': recent_appointments,
        'low_stock_products': low_stock_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'pending_revenue': pending_revenue,
        'recent_orders': recent_orders,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
@user_required
def user_dashboard(request):
    from appointments.models import Appointment
    
    appointments = Appointment.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'appointments': appointments,
    }
    return render(request, 'accounts/user_dashboard.html', context)


@login_required
def user_profile(request):
    from .forms import UserProfileForm
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'accounts/user_profile.html', context)


@login_required
@admin_required
def user_list(request):
    from django.core.paginator import Paginator
    
    users = User.objects.filter(role='user').order_by('-date_joined')
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_users': total_users,
        'active_users': active_users,
    }
    return render(request, 'accounts/user_list.html', context)


@login_required
@admin_required
def user_detail(request, pk):
    from appointments.models import Appointment
    
    user = get_object_or_404(User, pk=pk, role='user')
    user_appointments = Appointment.objects.filter(user=user).order_by('-created_at')
    
    total_appointments = user_appointments.count()
    pending_appointments = user_appointments.filter(status='pending').count()
    completed_appointments = user_appointments.filter(status='completed').count()
    cancelled_appointments = user_appointments.filter(status='cancelled').count()
    
    context = {
        'user_profile': user,
        'user_appointments': user_appointments,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
    }
    return render(request, 'accounts/user_detail.html', context)


@login_required
@admin_required
def reports(request):
    from products.models import Sale
    from django.core.paginator import Paginator
    from django.db.models import Sum, Count
    from django.utils import timezone
    
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    
    try:
        month = int(month)
        year = int(year)
    except:
        month = timezone.now().month
        year = timezone.now().year
    
    monthly_sales = Sale.objects.filter(sale_date__month=month, sale_date__year=year).aggregate(
        total_revenue=Sum('total_amount'), total_sales=Count('id'))
    monthly_revenue = monthly_sales['total_revenue'] or 0
    monthly_sales_count = monthly_sales['total_sales'] or 0
    
    yearly_sales = Sale.objects.filter(sale_date__year=year).aggregate(
        total_revenue=Sum('total_amount'), total_sales=Count('id'))
    yearly_revenue = yearly_sales['total_revenue'] or 0
    yearly_sales_count = yearly_sales['total_sales'] or 0
    
    all_sales = Sale.objects.all().select_related('product', 'customer')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_sales, 10)
    sales_page = paginator.get_page(page)
    
    months = [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
              (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')]
    years = range(2020, timezone.now().year + 1)
    
    context = {
        'monthly_revenue': monthly_revenue,
        'monthly_sales_count': monthly_sales_count,
        'yearly_revenue': yearly_revenue,
        'yearly_sales_count': yearly_sales_count,
        'sales_page': sales_page,
        'months': months,
        'years': years,
        'selected_month': month,
        'selected_year': year,
    }
    return render(request, 'accounts/reports.html', context)


def contact_us(request):
    from .forms import ContactForm
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact_us')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
                'phone': request.user.phone if request.user.phone != '0000000000' else '',
            }
        form = ContactForm(initial=initial_data)
    
    return render(request, 'accounts/contact_us.html', {'form': form})


@login_required
@admin_required
def contact_messages(request):
    from .models import Contact
    from django.core.paginator import Paginator
    
    status_filter = request.GET.get('status', 'all')
    contacts = Contact.objects.all()
    
    if status_filter == 'read':
        contacts = contacts.filter(is_read=True)
    elif status_filter == 'unread':
        contacts = contacts.filter(is_read=False)
    
    contacts = contacts.order_by('-created_at')
    
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_messages = Contact.objects.count()
    unread_messages = Contact.objects.filter(is_read=False).count()
    read_messages = Contact.objects.filter(is_read=True).count()
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'read_messages': read_messages,
    }
    
    return render(request, 'accounts/contact_messages.html', context)


@login_required
@admin_required
def mark_contact_read(request, contact_id):
    from .models import Contact
    
    if request.method == 'POST':
        contact = get_object_or_404(Contact, id=contact_id)
        contact.is_read = not contact.is_read
        contact.save()
        
        status = 'read' if contact.is_read else 'unread'
        messages.success(request, f'Message marked as {status}.')
    
    return redirect('contact_messages')


@login_required
def my_contact_requests(request):
    from .models import Contact
    from django.core.paginator import Paginator
    
    contacts = Contact.objects.filter(email=request.user.email).order_by('-created_at')
    
    total_count = contacts.count()
    replied_count = contacts.filter(admin_reply__isnull=False).exclude(admin_reply='').count()
    pending_count = total_count - replied_count
    
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_count': total_count,
        'replied_count': replied_count,
        'pending_count': pending_count,
    }
    
    return render(request, 'accounts/my_contact_requests.html', context)

