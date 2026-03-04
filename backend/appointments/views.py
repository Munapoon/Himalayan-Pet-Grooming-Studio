from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Service
from .forms import AppointmentForm
from accounts.decorators import admin_required


@login_required
def appointment_list(request):
    """List all appointments for the logged-in user"""
    from django.core.paginator import Paginator
    
    # Always show user's own appointments from navbar
    # Admin will use separate admin panel navigation
    appointments = Appointment.objects.filter(user=request.user).order_by('-created_at')
    template_name = 'appointments/appointment_list.html'
    
    # Pagination - 10 appointments per page
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, template_name, {'page_obj': page_obj})


@login_required
@admin_required
def admin_appointment_list(request):
    """Admin view to list all appointments"""
    from django.core.paginator import Paginator
    
    appointments = Appointment.objects.all().order_by('-created_at')
    
    # Pagination - 10 appointments per page
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'appointments/appointment_list_admin.html', {'page_obj': page_obj})


@login_required
@admin_required
def admin_appointment_detail(request, pk):
    """Admin view for appointment details"""
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail_admin.html', {'appointment': appointment})


@login_required
def appointment_detail(request, pk):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    if appointment.user != request.user:
        messages.error(request, 'You do not have permission to view this appointment.')
        return redirect('appointment_list')
    
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})


@login_required
def appointment_create(request):
    """Create a new appointment — redirects to advance payment after booking"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.advance_amount = 200  # Fixed advance
            appointment.payment_status = 'unpaid'
            appointment.save()
            messages.info(request, 'Almost done! Please pay the advance amount of Rs. 200 to confirm your booking.')

            # Redirect to home if coming from home page
            if request.POST.get('from_home'):
                request.session['pending_appointment'] = appointment.pk
                return redirect('appointment_payment', pk=appointment.pk)
            return redirect('appointment_payment', pk=appointment.pk)
        else:
            if request.POST.get('from_home'):
                for field, errors in form.errors.items():
                    for error in errors:
                        if field == '__all__':
                            messages.error(request, error)
                        else:
                            messages.error(request, f'{field.replace("_", " ").title()}: {error}')
                return redirect('home')
    else:
        service = request.GET.get('service')
        if service:
            form = AppointmentForm(initial={'service': service})
        else:
            form = AppointmentForm()

    return render(request, 'appointments/appointment_form.html', {'form': form, 'action': 'Create'})


@login_required
def appointment_payment(request, pk):
    """Show advance payment page for a booked appointment"""
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

    # Already paid — go to list
    if appointment.payment_status == 'paid':
        messages.success(request, 'Your appointment is already paid and booked!')
        return redirect('appointment_list')

    context = {
        'appointment': appointment,
        'advance_amount': appointment.advance_amount,
        'advance_paisa': int(appointment.advance_amount * 100),  # Khalti uses paisa
    }
    return render(request, 'appointments/appointment_payment.html', context)


@login_required
def appointment_khalti_verify(request):
    """Verify Khalti payment for appointment advance"""
    import requests as http_requests
    from django.conf import settings as django_settings

    if request.method == 'POST':
        token = request.POST.get('token')
        amount = request.POST.get('amount')
        appointment_pk = request.POST.get('appointment_id')

        appointment = get_object_or_404(Appointment, pk=appointment_pk, user=request.user)

        # Verify with Khalti
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {"token": token, "amount": amount}
        headers = {"Authorization": f"Key {getattr(django_settings, 'KHALTI_SECRET_KEY', '')}"}

        try:
            response = http_requests.post(url, payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                appointment.payment_status = 'paid'
                appointment.payment_method = 'khalti'
                appointment.khalti_transaction_id = data.get('idx', token)
                appointment.save()
                messages.success(
                    request,
                    f'Advance payment of Rs. {appointment.advance_amount} received! '
                    f'Your appointment is confirmed pending admin approval.'
                )
                return redirect('appointment_detail', pk=appointment.pk)
            else:
                messages.error(request, 'Payment verification failed. Please try again or contact us.')
                return redirect('appointment_payment', pk=appointment.pk)
        except Exception as e:
            messages.error(request, f'Payment error: {str(e)}')
            return redirect('appointment_payment', pk=appointment.pk)

    return redirect('appointment_list')


@login_required
def appointment_update(request, pk):
    """Update an existing appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    if not request.user.is_admin_user() and appointment.user != request.user:
        messages.error(request, 'You do not have permission to edit this appointment.')
        return redirect('appointment_list')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointments/appointment_form.html', {'form': form, 'action': 'Update'})


@login_required
def appointment_delete(request, pk):
    """Delete an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    if not request.user.is_admin_user() and appointment.user != request.user:
        messages.error(request, 'You do not have permission to delete this appointment.')
        return redirect('appointment_list')
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('appointment_list')
    
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})


@login_required
@admin_required
def appointment_update_status(request, pk):
    """Admin can update appointment status"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Appointment.STATUS_CHOICES):
            appointment.status = status
            appointment.save()
            messages.success(request, f'Appointment status updated to {appointment.get_status_display()}!')
        return redirect('admin_dashboard')
    
    return redirect('appointment_list')


@login_required
def service_detail(request, service_type):
    """View service details with reviews — data from the Service DB model."""
    from .models import ServiceReview
    from django.db.models import Avg

    # Validate service type
    valid_slugs = [s[0] for s in Appointment.SERVICE_CHOICES]
    if service_type not in valid_slugs:
        messages.error(request, 'Invalid service type.')
        return redirect('home')

    # Fetch from DB (fallback if not yet seeded)
    service_obj = Service.objects.filter(slug=service_type, is_active=True).first()

    # Build a service_details dict the template already expects
    if service_obj:
        service_name = service_obj.name
        service_details = {
            'image':       service_obj.image_url,
            'description': service_obj.description,
            'price':       service_obj.price,
            'duration':    service_obj.duration,
            'features':    service_obj.features,  # list from JSON
        }
    else:
        # Fallback to choice label if DB row missing
        service_name = dict(Appointment.SERVICE_CHOICES).get(service_type, service_type)
        service_details = {}

    # Check if user has completed this service
    has_used_service = Appointment.objects.filter(
        user=request.user,
        service=service_type,
        status='completed'
    ).exists()

    # Check if user already reviewed this service
    user_review = ServiceReview.objects.filter(
        user=request.user,
        service=service_type
    ).first()

    # Get all reviews for this service
    reviews = ServiceReview.objects.filter(service=service_type).select_related('user')

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = reviews.count()

    # Get rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        count = reviews.filter(rating=i).count()
        percentage = (count * 100 / total_reviews) if total_reviews > 0 else 0
        rating_distribution[i] = {
            'count': count,
            'percentage': round(percentage, 1)
        }

    # All active services for the sidebar navigation
    all_services = Service.objects.filter(is_active=True).order_by('order')

    context = {
        'service_type':    service_type,
        'service_name':    service_name,
        'service_details': service_details,
        'service_obj':     service_obj,
        'has_used_service': has_used_service,
        'user_review':     user_review,
        'reviews':         reviews,
        'avg_rating':      round(avg_rating, 1),
        'total_reviews':   total_reviews,
        'rating_distribution': rating_distribution,
        'all_services':    all_services,
    }

    return render(request, 'appointments/service_detail.html', context)


@login_required
def add_service_review(request, service_type):
    """Add or update service review"""
    from .models import ServiceReview
    
    # Check if user has completed this service
    has_used_service = Appointment.objects.filter(
        user=request.user,
        service=service_type,
        status='completed'
    ).exists()
    
    if not has_used_service:
        messages.error(request, 'You can only review services you have used.')
        return redirect('service_detail', service_type=service_type)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        if not rating or not review_text:
            messages.error(request, 'Please provide both rating and review.')
            return redirect('service_detail', service_type=service_type)
        
        # Create or update review
        review, created = ServiceReview.objects.update_or_create(
            user=request.user,
            service=service_type,
            defaults={
                'rating': int(rating),
                'review': review_text,
            }
        )
        
        if created:
            messages.success(request, 'Thank you for your review!')
        else:
            messages.success(request, 'Your review has been updated!')
        
        return redirect('service_detail', service_type=service_type)
    
    return redirect('service_detail', service_type=service_type)


@login_required
@admin_required
def appointment_confirm(request, pk):
    """Admin can confirm a pending appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        if appointment.status == 'pending':
            appointment.status = 'confirmed'
            appointment.save()
            messages.success(request, f'Appointment for {appointment.pet_name} has been confirmed!')
        else:
            messages.warning(request, f'This appointment is already {appointment.get_status_display()}.')
        
        # Check if coming from detail page
        if request.POST.get('from_detail'):
            return redirect('admin_appointment_detail', pk=pk)
        return redirect('admin_appointment_list')
    
    return redirect('appointment_list')


@login_required
@admin_required
def appointment_complete(request, pk):
    """Admin can mark a confirmed appointment as completed"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        if appointment.status == 'confirmed':
            appointment.status = 'completed'
            appointment.save()
            messages.success(request, f'Appointment for {appointment.pet_name} has been marked as completed!')
        else:
            messages.warning(request, f'Only confirmed appointments can be completed. Current status: {appointment.get_status_display()}.')
        
        # Check if coming from detail page
        if request.POST.get('from_detail'):
            return redirect('admin_appointment_detail', pk=pk)
        return redirect('admin_appointment_list')
    
    return redirect('admin_appointment_list')


@login_required
@admin_required
def admin_service_review_list(request):
    """Admin view to list all service reviews"""
    from .models import ServiceReview
    from django.core.paginator import Paginator
    from django.db.models import Avg, Count
    
    # Get filter parameters
    service_filter = request.GET.get('service', '')
    rating_filter = request.GET.get('rating', '')
    
    # Base queryset
    reviews = ServiceReview.objects.all().select_related('user', 'appointment').order_by('-created_at')
    
    # Apply filters
    if service_filter:
        reviews = reviews.filter(service=service_filter)
    if rating_filter:
        reviews = reviews.filter(rating=int(rating_filter))
    
    # Statistics
    total_reviews = ServiceReview.objects.count()
    avg_rating = ServiceReview.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Service-wise stats
    service_stats = []
    for code, name in Appointment.SERVICE_CHOICES:
        service_reviews = ServiceReview.objects.filter(service=code)
        count = service_reviews.count()
        avg = service_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        service_stats.append({
            'code': code,
            'name': name,
            'count': count,
            'avg_rating': round(avg, 1)
        })
    
    # Pagination
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 1),
        'service_stats': service_stats,
        'service_choices': Appointment.SERVICE_CHOICES,
        'service_filter': service_filter,
        'rating_filter': rating_filter,
    }
    
    return render(request, 'appointments/admin_service_review_list.html', context)


def service_list(request):
    """Public view to list all grooming services — data from the Service DB model."""
    from .models import ServiceReview
    from django.db.models import Avg
    from django.core.paginator import Paginator

    # Fetch active services from DB ordered by display order
    services_list = Service.objects.filter(is_active=True).order_by('order')

    # Pagination - 5 services per page (puts new ones on page 2)
    paginator = Paginator(services_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Attach avg_rating and review_count to each service object in current page
    service_ratings = {}
    for svc in page_obj:
        reviews = ServiceReview.objects.filter(service=svc.slug)
        avg = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        count = reviews.count()
        svc.avg_rating = round(avg, 1) if avg else 0
        svc.review_count = count
        service_ratings[svc.slug] = {
            'avg_rating': svc.avg_rating,
            'review_count': count,
        }

    context = {
        'services':        page_obj,
        'page_obj':        page_obj,
        'service_ratings': service_ratings,
    }
    return render(request, 'appointments/service_list.html', context)


@login_required
@admin_required
def admin_service_list(request):
    """Admin view to manage grooming services."""
    services = Service.objects.all().order_by('order', 'name')
    return render(request, 'appointments/admin_service_list.html', {'services': services})


@login_required
@admin_required
def admin_service_add(request):
    """Admin view to add a new grooming service."""
    from .forms import ServiceForm
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully.')
            return redirect('admin_service_list')
    else:
        form = ServiceForm()
    return render(request, 'appointments/admin_service_form.html', {'form': form, 'title': 'Add Service'})


@login_required
@admin_required
def admin_service_edit(request, pk):
    """Admin view to edit an existing grooming service."""
    from .forms import ServiceForm
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service "{service.name}" updated successfully.')
            return redirect('admin_service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'appointments/admin_service_form.html', {'form': form, 'title': f'Edit Service: {service.name}'})


@login_required
@admin_required
def admin_service_delete(request, pk):
    """Admin view to delete a grooming service."""
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
         service.delete()
         messages.success(request, f'Service "{service.name}" deleted successfully.')
         return redirect('admin_service_list')
    return render(request, 'appointments/admin_service_confirm_delete.html', {'service': service})
