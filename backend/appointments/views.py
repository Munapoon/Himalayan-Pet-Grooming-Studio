from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
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
    """Create a new appointment"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            
            # Redirect to home if coming from home page
            if request.POST.get('from_home'):
                return redirect('home')
            return redirect('appointment_list')
        else:
            # If coming from home page and form has errors, redirect back with form
            if request.POST.get('from_home'):
                # Add error messages
                for field, errors in form.errors.items():
                    for error in errors:
                        if field == '__all__':
                            messages.error(request, error)
                        else:
                            messages.error(request, f'{field.replace("_", " ").title()}: {error}')
                return redirect('home')
    else:
        # Get service from URL parameter
        service = request.GET.get('service')
        if service:
            form = AppointmentForm(initial={'service': service})
        else:
            form = AppointmentForm()
    
    return render(request, 'appointments/appointment_form.html', {'form': form, 'action': 'Create'})


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
    """View service details with reviews"""
    from .models import ServiceReview
    from django.db.models import Avg, Count
    
    # Get service info
    service_choices = dict(Appointment._meta.get_field('service').choices)
    if service_type not in service_choices:
        messages.error(request, 'Invalid service type.')
        return redirect('home')
    
    service_name = service_choices[service_type]
    
    # Service details with images and descriptions
    service_info = {
        'bath': {
            'image': 'https://images.unsplash.com/photo-1558788353-f76d92427f16?w=800',
            'description': 'Complete bath service with premium shampoo, conditioning, blow-dry, and brush-out. Perfect for keeping your pet clean and fresh.',
            'price': 'Rs. 950 - Rs. 2250',
            'duration': '45-90 minutes',
            'features': [
                'Premium pet shampoo & conditioner',
                'Thorough brush-out',
                'Professional blow-dry',
                'Nail trimming included',
                'Ear cleaning',
                'Paw pad moisturizing'
            ]
        },
        'haircut': {
            'image': 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=800',
            'description': 'Professional haircut and styling tailored to your pet\'s breed and your preferences. Our expert groomers ensure your pet looks their best.',
            'price': 'Rs. 1200',
            'duration': '60-120 minutes',
            'features': [
                'Breed-specific cuts',
                'Custom styling',
                'Face & feet trim',
                'Sanitary trim',
                'Full body scissoring',
                'Finishing touches'
            ]
        },
        'nails': {
            'image': 'https://images.unsplash.com/photo-1611850968574-de37a1f28b11?w=800',
            'description': 'Professional nail trimming and filing service to keep your pet comfortable and prevent scratching.',
            'price': 'Starting at Rs. 300',
            'duration': '15-30 minutes',
            'features': [
                'Precise nail trimming',
                'Smooth filing',
                'Quick check included',
                'Paw pad inspection',
                'Gentle handling',
                'Stress-free experience'
            ]
        },
        'full': {
            'image': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800',
            'description': 'Our most comprehensive grooming package combining bath, haircut, and all finishing touches for a complete transformation.',
            'price': 'Rs. 1500 - Rs. 2950',
            'duration': '2-3 hours',
            'features': [
                'Full bath & conditioning',
                'Complete haircut styling',
                'Nail trim & filing',
                'Teeth brushing',
                'Ear cleaning & care',
                'Paw pad trim',
                'Luxury cologne application',
                'Decorative bow or bandana'
            ]
        },
        'spa': {
            'image': 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=800',
            'description': 'Luxury spa treatment for your beloved pet. Includes massage, aromatherapy, and premium grooming products for ultimate relaxation.',
            'price': 'Rs. 2000 - Rs. 3500',
            'duration': '2-3 hours',
            'features': [
                'Aromatherapy bath',
                'Relaxing massage',
                'Premium spa products',
                'Hot towel treatment',
                'Pawdicure service',
                'Facial treatment',
                'Calming essential oils',
                'Luxury finishing'
            ]
        }
    }
    
    service_details = service_info.get(service_type, {})
    
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
    
    context = {
        'service_type': service_type,
        'service_name': service_name,
        'service_details': service_details,
        'has_used_service': has_used_service,
        'user_review': user_review,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'total_reviews': total_reviews,
        'rating_distribution': rating_distribution,
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
