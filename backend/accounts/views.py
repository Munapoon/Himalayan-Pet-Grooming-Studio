from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q, Min, Count
from django.utils import timezone
from datetime import timedelta
import random

from .models import User, Contact
from products.models import Order
from appointments.models import Appointment
from .forms import (
    UserRegistrationForm, UserLoginForm, ForgotPasswordForm, 
    VerifyResetCodeForm, ResetPasswordForm, ChangePasswordForm,
    UserProfileForm, VerifyEmailForm
)
from .decorators import admin_required


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                user.reset_code = code
                user.reset_code_expires_at = timezone.now() + timedelta(minutes=5)
                user.save()
                
                request.session['reset_email'] = email
                
                try:
                    context = {
                        'user_name': user.username,
                        'verification_code': code,
                        'title': 'Password Reset Request',
                        'intro_text': 'We received a request to reset your password. Use the code below to proceed with the reset process:'
                    }
                    html_message = render_to_string('emails/verification_email.html', context)
                    plain_message = strip_tags(html_message)
                    
                    send_mail(
                        'Password Reset - Himalayan Pet Studio',
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                except Exception as e:
                    messages.warning(request, f"Email failed to send: {str(e)}. Check console.")
                
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
                    request.session['reset_email'] = email
                    return redirect('reset_password')
                else:
                    messages.error(request, 'Error: "This code has expired"')
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
                
                del request.session['reset_email']
                messages.success(request, "Password has been reset successfully. Please login.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "Something went wrong.")
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
                login(request, user)
                messages.success(request, "Your password has been changed successfully.")
                return redirect('user_profile')
            else:
                form.add_error('old_password', 'Current password is incorrect.')
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/change_password.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user():
            return redirect('admin_dashboard')
        elif request.user.is_staff_user():
            return redirect('staff_dashboard')
    
    from appointments.models import Service, ServiceReview
    from django.db.models import Avg, Count
    
    services = Service.objects.filter(is_active=True).order_by('order')
    
    
    service_ratings = {}
    for svc in services:
        reviews = ServiceReview.objects.filter(service=svc.slug)
        avg = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        svc.avg_rating = round(avg, 1)
        svc.review_count = reviews.count()
        service_ratings[svc.slug] = {'avg_rating': svc.avg_rating, 'review_count': svc.review_count}
    
    from products.models import Product
    top_rated_products = Product.objects.filter(is_active=True, stock_quantity__gt=0).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(review_count__gt=0).order_by('-avg_rating')[:8]
    
    top_products = Product.objects.filter(is_active=True, stock_quantity__gt=0).annotate(
        total_sold=Count('orderitem')
    ).filter(total_sold__gt=0).order_by('-total_sold')[:5]
    
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
        elif request.user.is_staff_user():
            return redirect('staff_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                is_first_login = user.last_login is None
                
                login(request, user)
                
                
                if is_first_login:
                    try:
                        context = {
                            'user_name': user.username,
                            'site_url': request.build_absolute_uri('/')[:-1]
                        }
                        html_message = render_to_string('emails/welcome_email.html', context)
                        plain_message = strip_tags(html_message)
                        
                        send_mail(
                            'Welcome to Himalayan Pet Studio!',
                            plain_message,
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            html_message=html_message,
                            fail_silently=False,
                        )
                    except Exception as e:
                        print(f"Failed to send welcome email: {e}")


                messages.success(request, 'Login successful')
                if user.is_admin_user():
                    return redirect('admin_dashboard')
                elif user.is_staff_user():
                    return redirect('staff_dashboard')
                return redirect('home')
            else:
                
                try:
                    user_check = User.objects.get(username=username)
                    if not user_check.is_active and user_check.check_password(password):
                        messages.warning(request, 'Please verify your email address first.')
                        request.session['verification_email'] = user_check.email
                        return redirect('verify_email')
                except User.DoesNotExist:
                    pass
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
            user.is_active = False 
            
            
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            user.verification_code = code
            user.save()
            
            
            try:
                context = {
                    'user_name': user.username,
                    'verification_code': code,
                    'title': 'Welcome to Himalayan Pet Studio',
                    'intro_text': 'Thank you for signing up! To complete your registration and verify your email, please use the code below:'
                }
                html_message = render_to_string('emails/verification_email.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    'Email Verification - Himalayan Pet Studio',
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send verification email: {e}")

            request.session['verification_email'] = user.email
            messages.success(request, 'Registration successful. A verification code has been sent to your email.')
            return redirect('verify_email')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request):
    email = request.session.get('verification_email')
    if not email:
        return redirect('register')
        
    if request.method == 'POST':
        form = VerifyEmailForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(email=email, verification_code=code)
                user.is_email_verified = True
                user.is_active = True
                user.verification_code = None
                user.save()
                
                del request.session['verification_email']
                messages.success(request, "Email verified successfully! Please login to your account.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "Invalid verification code.")
    else:
        form = VerifyEmailForm(initial={'email': email})
    return render(request, 'accounts/verify_email.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@login_required
@admin_required
def admin_dashboard(request):
    from appointments.models import Appointment, Service
    from products.models import Product, Order, Payment
    from django.utils import timezone
    from datetime import timedelta
    import json

    total_users = User.objects.count()
    total_bookings = Appointment.objects.count()
    total_services = Service.objects.count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    tasks_percentage = int((completed_appointments / total_bookings) * 100) if total_bookings > 0 else 0
    pending_appointments = Appointment.objects.filter(status='pending').count()
    recent_appointments = Appointment.objects.select_related('user').all().order_by('-created_at')[:5]
    low_stock_products = Product.objects.filter(stock_quantity__lt=10).order_by('stock_quantity')[:5]

    
    import calendar
    from decimal import Decimal
    from django.db.models import Sum

    total_revenue = Payment.objects.filter(
        status__in=['completed', 'refunded']
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    
    today = timezone.now().date()
    import calendar
    from decimal import Decimal
    
    months_labels = []
    earnings_data = []
    appointment_data = []
    
    from datetime import date, datetime
    
    for i in range(5, -1, -1):
        
        m = today.month - i
        y = today.year
        while m <= 0:
            m += 12
            y -= 1
        
        target_date = date(y, m, 1)
        months_labels.append(target_date.strftime('%b'))
        
        
        last_day = calendar.monthrange(y, m)[1]
        start_date = timezone.make_aware(datetime(y, m, 1))
        end_date = timezone.make_aware(datetime(y, m, last_day, 23, 59, 59))
        
        
        month_revenue = Payment.objects.filter(
            created_at__range=(start_date, end_date),
            status__in=['completed', 'refunded']
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        earnings_data.append(float(month_revenue))
        
        
        a_count = Appointment.objects.filter(
            created_at__range=(start_date, end_date),
            status__in=['pending', 'confirmed', 'completed']
        ).count()
        appointment_data.append(a_count)

    chart_data = {
        'labels': months_labels,
        'earnings': earnings_data,
        'appointments': appointment_data,
    }

    context = {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_services': total_services,
        'tasks_percentage': tasks_percentage,
        'pending_appointments': pending_appointments,
        'recent_appointments': recent_appointments,
        'low_stock_products': low_stock_products,
        'total_revenue': float(total_revenue),
        'chart_data_json': json.dumps(chart_data),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def user_dashboard(request):
    if request.user.is_admin_user():
        return redirect('admin_dashboard')
    elif request.user.is_staff_user():
        return redirect('staff_dashboard')
    
    
    return redirect('user_profile')

@login_required
def staff_dashboard(request):
    if not request.user.is_staff_user() and not request.user.is_admin_user():
        messages.error(request, "Access denied.")
        return redirect('home')
        
    from appointments.models import Appointment
    from datetime import date
    
    today = date.today()
    
    today_appointments = Appointment.objects.filter(
        assigned_staff=request.user, 
        appointment_date=today
    ).order_by('appointment_time')
    
    
    upcoming_appointments = Appointment.objects.filter(
        assigned_staff=request.user,
        appointment_date__gt=today
    ).exclude(status='completed').order_by('appointment_date', 'appointment_time')[:10]
    
    
    completed_today = today_appointments.filter(status='completed').count()
    pending_today = today_appointments.exclude(status='completed').count()
    total_completed_all_time = Appointment.objects.filter(assigned_staff=request.user, status='completed').count()

    context = {
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'completed_today': completed_today,
        'pending_today': pending_today,
        'total_completed_all_time': total_completed_all_time,
    }
    return render(request, 'accounts/staff_dashboard.html', context)


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

    total_appointments = Appointment.objects.filter(user=request.user).count()
    total_orders = Order.objects.filter(user=request.user).count()
    
    context = {
        'form': form,
        'total_appointments': total_appointments,
        'total_orders': total_orders,
        'member_points': total_orders * 10,
    }
    return render(request, 'accounts/user_profile.html', context)


@login_required
def remove_profile_picture(request):
    """Remove user's profile picture"""
    user = request.user
    if user.profile_picture:
        user.profile_picture.delete(save=False) 
        user.profile_picture = None
        user.save()
        messages.success(request, 'Profile picture removed.')
    else:
        messages.info(request, 'No profile picture to remove.')
    return redirect('user_profile')


@login_required
@admin_required
def user_list(request):
    users_list = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users_list, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'accounts/user_list.html', {'users': page_obj, 'page_obj': page_obj})


@login_required
@admin_required
def user_detail(request, pk):
    user_profile = get_object_or_404(User, pk=pk)
    user_appointments = Appointment.objects.filter(user=user_profile).order_by('-created_at')
    
    context = {
        'user_profile': user_profile,
        'user_appointments': user_appointments,
        'total_appointments': user_appointments.count(),
        'pending_appointments': user_appointments.filter(status='pending').count(),
        'completed_appointments': user_appointments.filter(status='completed').count(),
        'cancelled_appointments': user_appointments.filter(status='cancelled').count(),
    }
    return render(request, 'accounts/user_detail.html', context)


@login_required
@admin_required
def user_update_role(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in ['admin', 'staff', 'user']:
            user_obj.role = new_role
            
            if new_role == 'admin':
                user_obj.is_superuser = True
                user_obj.is_staff = True
            elif new_role == 'staff':
                user_obj.is_superuser = False
                user_obj.is_staff = True
            else: 
                user_obj.is_superuser = False
                user_obj.is_staff = False
                
            user_obj.save()
            messages.success(request, f"User {user_obj.username}'s role was updated to {new_role}.")
    return redirect('user_detail', pk=pk)


@login_required
@admin_required
def reports(request):
    from products.models import Payment
    import calendar
    from datetime import datetime

    now = timezone.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))

    all_sales = Payment.objects.filter(status__in=['completed', 'refunded'])
    
    from datetime import datetime
    month_last_day = calendar.monthrange(selected_year, selected_month)[1]
    
    if timezone.is_aware(now):
        start_date = timezone.make_aware(datetime(selected_year, selected_month, 1))
        end_date = timezone.make_aware(datetime(selected_year, selected_month, month_last_day, 23, 59, 59))
        start_year_date = timezone.make_aware(datetime(selected_year, 1, 1))
        end_year_date = timezone.make_aware(datetime(selected_year, 12, 31, 23, 59, 59))
    else:
        start_date = datetime(selected_year, selected_month, 1)
        end_date = datetime(selected_year, selected_month, month_last_day, 23, 59, 59)
        start_year_date = datetime(selected_year, 1, 1)
        end_year_date = datetime(selected_year, 12, 31, 23, 59, 59)

    
    monthly_sales = all_sales.filter(created_at__range=(start_date, end_date))
    
    monthly_revenue = monthly_sales.aggregate(total=Sum('amount'))['total'] or 0
    product_monthly_revenue = monthly_sales.filter(order__isnull=False).aggregate(total=Sum('amount'))['total'] or 0
    service_monthly_revenue = monthly_sales.filter(appointment__isnull=False).aggregate(total=Sum('amount'))['total'] or 0

    yearly_sales = all_sales.filter(created_at__range=(start_year_date, end_year_date))
    yearly_revenue = yearly_sales.aggregate(total=Sum('amount'))['total'] or 0
    product_yearly_revenue = yearly_sales.filter(order__isnull=False).aggregate(total=Sum('amount'))['total'] or 0
    service_yearly_revenue = yearly_sales.filter(appointment__isnull=False).aggregate(total=Sum('amount'))['total'] or 0

    service_name_map = dict(Appointment.SERVICE_CHOICES)
    sales_qs = monthly_sales.select_related('order', 'appointment', 'user').order_by('-created_at')

    
    from collections import defaultdict
    daily_stats = defaultdict(lambda: {"total": 0, "count": 0})
    
    for sale in sales_qs:
        date_str = timezone.localtime(sale.created_at).date().strftime('%b %d, %Y')
        daily_stats[date_str]["total"] += float(sale.amount)
        daily_stats[date_str]["count"] += 1
        
    daily_summary = []
    for date_str, stats in sorted(daily_stats.items()):
        daily_summary.append({
            'date': date_str,
            'total': stats['total'],
            'count': stats['count'],
            'percentage': (stats['total'] / float(monthly_revenue) * 100) if monthly_revenue > 0 else 0
        })

    enriched_sales = []
    for p in sales_qs:
        name, category_name, qty, unit_price = "Misc", "Revenue", 1, float(p.amount)
        if p.order:
            items = list(p.order.items.all()[:2])
            item_names = ", ".join([it.product.name for it in items])
            if p.order.items.count() > 2: item_names += " ..."
            name = f"Order #{p.order.order_number} ({item_names})"
            qty = sum([it.quantity for it in p.order.items.all()]) or 1
            unit_price = float(p.amount) / qty
            category_name = "E-Commerce"
        elif p.appointment:
            svc_name = service_name_map.get(p.appointment.service, p.appointment.service)
            name = f"Grooming: {svc_name} ({p.appointment.pet_name})"
            category_name = "Grooming"

        enriched_sales.append({
            'id': p.id,
            'product': {'name': name, 'category': {'name': category_name}},
            'customer': p.user,
            'quantity': qty,
            'unit_price': round(unit_price, 2),
            'total_amount': float(p.amount),
            'payment_method': p.payment_method,
            'sale_date': p.created_at,
        })

    paginator = Paginator(enriched_sales, 10)
    sales_page = paginator.get_page(request.GET.get('page'))

    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    min_year_obj = all_sales.aggregate(Min('created_at'))['created_at__min']
    start_year = min_year_obj.year if min_year_obj else now.year - 4

    context = {
        'months': months, 'years': range(start_year, now.year + 1),
        'selected_month': selected_month, 'selected_year': selected_year,
        'monthly_revenue': float(monthly_revenue),
        'product_monthly_revenue': float(product_monthly_revenue),
        'service_monthly_revenue': float(service_monthly_revenue),
        'yearly_revenue': float(yearly_revenue),
        'product_yearly_revenue': float(product_yearly_revenue),
        'service_yearly_revenue': float(service_yearly_revenue),
        'sales_page': sales_page,
        'daily_summary': daily_summary,
    }
    return render(request, 'accounts/reports.html', context)


@login_required
@admin_required
def export_sales_csv(request):
    import csv
    import calendar
    from django.http import HttpResponse
    from products.models import Payment
    from appointments.models import Appointment
    from datetime import datetime

    now = datetime.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Sales_Report_{calendar.month_name[selected_month]}_{selected_year}.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Source', 'Detail', 'Customer', 'Amount', 'Method', 'Date', 'Time'])

    service_name_map = dict(Appointment.SERVICE_CHOICES)
    
    from django.utils import timezone
    month_last_day = calendar.monthrange(selected_year, selected_month)[1]
    
    if timezone.is_aware(now):
        start_date = timezone.make_aware(datetime(selected_year, selected_month, 1))
        end_date = timezone.make_aware(datetime(selected_year, selected_month, month_last_day, 23, 59, 59))
    else:
        start_date = datetime(selected_year, selected_month, 1)
        end_date = datetime(selected_year, selected_month, month_last_day, 23, 59, 59)
    
    payments = Payment.objects.filter(
        status__in=['completed', 'refunded'],
        created_at__range=(start_date, end_date)
    ).select_related('order', 'appointment', 'user').order_by('-created_at')

    for p in payments:
        source, detail = "Misc", "N/A"
        if p.order:
            source = f"Order #{p.order.order_number}"
            detail = ", ".join([it.product.name for it in p.order.items.all()[:3]])
        elif p.appointment:
            source = "Grooming"
            svc_name = service_name_map.get(p.appointment.service, p.appointment.service)
            detail = f"{svc_name} ({p.appointment.pet_name})"

        customer_name = (p.user.get_full_name() or p.user.username) if p.user else "Walk-in"
        writer.writerow([
            p.id, 
            source, 
            detail, 
            customer_name,
            p.amount, 
            p.get_payment_method_display(), 
            p.created_at.strftime('%Y-%m-%d'), 
            p.created_at.strftime('%H:%M')
        ])
    return response


@login_required
@admin_required
def contact_messages(request):
    messages_list = Contact.objects.all().order_by('-created_at')
    
    
    unread_count = Contact.objects.filter(is_read=False).count()
    
    read_count = Contact.objects.filter(is_read=True, admin_reply__isnull=True).exclude(admin_reply__exact='').count()
    
    replied_count = Contact.objects.exclude(admin_reply__isnull=True).exclude(admin_reply__exact='').count()
    high_priority_count = Contact.objects.filter(priority='High').count()

    paginator = Paginator(messages_list, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'accounts/contact_messages.html', {
        'contact_messages_list': page_obj, 
        'page_obj': page_obj, 
        'unread_count': unread_count,
        'read_count': read_count,
        'replied_count': replied_count,
        'high_priority_count': high_priority_count
    })


def contact_us(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.')
            return redirect('login')
        Contact.objects.create(
            name=request.POST.get('name'), email=request.POST.get('email'),
            phone=request.POST.get('phone', ''), subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        messages.success(request, 'Message sent!')
        return redirect('contact_us')
        
    
    faqs = [
        {
            'question': 'How can I book an appointment?',
            'answer': 'You can book an appointment by navigating to the Services page or directly from your user dashboard after logging in.'
        },
        {
            'question': 'What are your operating hours?',
            'answer': 'We are open Sunday through Friday, from 10:00 AM to 6:00 PM.'
        },
        {
            'question': 'Do you offer mobile grooming?',
            'answer': 'Currently, we only offer services at our studio located in Amar Singh Chowk, Pokhara.'
        },
        {
            'question': 'Are your products pet-friendly?',
            'answer': 'Yes, all our grooming products are eco-friendly, organic, and specifically chosen to be safe for sensitive pet skin.'
        },
        {
            'question': 'How do I pay for my service?',
            'answer': 'You can pay online via Khalti during booking or pay in person with cash at the studio after the grooming session.'
        }
    ]
    
    return render(request, 'contact.html', {'faqs': faqs})


@login_required
def my_contact_requests(request):
    return render(request, 'accounts/my_contact_request.html', {'messages_list': Contact.objects.filter(email=request.user.email).order_by('-id')})


@login_required
@admin_required
def user_toggle_status(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if user_obj.is_superuser:
        messages.error(request, "Cannot deactivate superuser.")
    else:
        user_obj.is_active = not user_obj.is_active
        user_obj.save()
        messages.success(request, f"User {user_obj.username} status updated.")
    return redirect('user_detail', pk=pk)


@login_required
@admin_required
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if user_obj.is_superuser:
        messages.error(request, "Cannot delete superuser.")
    else:
        user_obj.delete()
        messages.success(request, "User deleted.")
    return redirect('user_list')


@login_required
@admin_required
def mark_contact_read(request, pk):
    message = get_object_or_404(Contact, pk=pk)
    message.is_read = True
    message.save()
    from django.http import JsonResponse
    return JsonResponse({'status': 'success'})


@login_required
@admin_required
def delete_contact(request, pk):
    message = get_object_or_404(Contact, pk=pk)
    message.delete()
    messages.success(request, 'Message deleted successfully.')
    return redirect('contact_messages')


@login_required
@admin_required
def staff_search(request):
    query = request.GET.get('q', '').strip()
    appointments, orders, users = [], [], []
    if query:
        appointments = Appointment.objects.filter(Q(id__icontains=query) | Q(pet_name__icontains=query) | Q(user__username__icontains=query))[:10]
        orders = Order.objects.filter(Q(order_number__icontains=query) | Q(user__username__icontains=query))[:10]
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))[:10]
    return render(request, 'accounts/staff_search_results.html', {'query': query, 'appointments': appointments, 'orders': orders, 'users': users})


def about_us(request):
    """View to render the About Us page."""
    return render(request, 'about.html')


def legal(request):
    """View to render the Legal/Terms & Conditions page."""
    return render(request, 'legal.html')
