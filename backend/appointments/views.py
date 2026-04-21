from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
import requests as http_requests
import json
import decimal
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Appointment, Service, ServiceReview, Pet
from .forms import AppointmentForm, PetForm
from accounts.decorators import admin_required


@login_required
def appointment_list(request):
    """List all appointments for the logged-in user"""
    
    # Always show user's own appointments from navbar
    # Admin will use separate admin panel navigation
    # Hide appointments that are still waiting for advance payment (unconfirmed bookings)
    appointments = Appointment.objects.filter(
        user=request.user
    ).exclude(
        payment_status='pending_payment'
    ).order_by('-created_at')
    template_name = 'appointments/appointment_list.html'
    
    # Pagination - 15 appointments per page
    paginator = Paginator(appointments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, template_name, {'page_obj': page_obj})


@login_required
@admin_required
def admin_appointment_list(request):
    """Admin view to list all appointments"""
    from django.core.paginator import Paginator
    
    # Hide fake/abandoned waitlist (unconfirmed payments) from admin dashboard
    appointments = Appointment.objects.exclude(payment_status='pending_payment').order_by('-created_at')
    
    # Pagination - 15 appointments per page
    paginator = Paginator(appointments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'appointments/appointment_list_admin.html', {'page_obj': page_obj})


@login_required
@admin_required
def admin_appointment_detail(request, pk):
    """Admin view for appointment details"""
    from .forms import AppointmentForm
    from accounts.models import User
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        staff_id = request.POST.get('assigned_staff')
        if staff_id:
            try:
                staff_user = User.objects.get(pk=staff_id, role='staff')
                appointment.assigned_staff = staff_user
                appointment.save()
                messages.success(request, f'Successfully assigned to {staff_user.username}.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid staff member selected.')
        else:
            appointment.assigned_staff = None
            appointment.save()
            messages.success(request, 'Staff assignment removed.')
        return redirect('admin_appointment_detail', pk=pk)

    form = AppointmentForm(instance=appointment)
    staff_members = User.objects.filter(role='staff', is_active=True)
    
    payments = appointment.payments.all().order_by('-created_at')
    
    return render(request, 'appointments/appointment_detail_admin.html', {
        'appointment': appointment,
        'form': form,
        'staff_members': staff_members,
        'payments': payments
    })


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
    # Prevent admins from booking manually as per requirement
    if request.user.role == 'admin':
        messages.error(request, 'Administrators cannot book appointments manually. Please use a customer account.')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.advance_amount = 10  # Fixed advance
            appointment.payment_status = 'pending_payment'  # Not confirmed until paid
            appointment.save()
            # Redirect directly to payment — no message yet, slot not confirmed
            return redirect('appointment_payment', pk=appointment.pk)
        else:
            # Existing error handling...
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

    user_pets = Pet.objects.filter(user=request.user)
    base_template = 'admin_base.html' if request.user.is_admin_user() else 'base.html'
    return render(request, 'appointments/appointment_form.html', {
        'form': form, 
        'action': 'Create', 
        'base_template': base_template,
        'user_pets': user_pets
    })


@login_required
def appointment_payment(request, pk):
    """Show advance payment summary before redirecting to Khalti"""
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

    # If already paid, nothing to do
    if appointment.payment_status in ('advance_paid', 'paid'):
        messages.success(request, 'Your appointment is already paid!')
        return redirect('appointment_list')

    context = {
        'appointment': appointment,
        'advance_amount': appointment.advance_amount,
    }
    return render(request, 'appointments/appointment_payment.html', context)


@login_required
def appointment_khalti_initiate(request, pk):
    """
    KPG-2 Initiate: Called when user clicks 'Pay' button.
    Redirects to Khalti.
    """
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

    url = f"{django_settings.KHALTI_BASE_URL}epayment/initiate/"
    return_url = request.build_absolute_uri(reverse('appointment_khalti_verify'))
    
    payload = {
        "return_url": return_url,
        "website_url": request.build_absolute_uri('/'),
        "amount": int(appointment.advance_amount * 100),
        "purchase_order_id": f"appt-{appointment.pk}",
        "purchase_order_name": f"Booking #{appointment.id}: {appointment.get_service_display()} for {appointment.pet_name}",
        "customer_info": {
            "name": request.user.get_full_name() or request.user.username,
            "email": request.user.email or "customer@example.com",
            # Fallback phone if model doesn't have it
            "phone": getattr(request.user, 'phone', '9800000000') or '9800000000'
        }
    }
    
    headers = {
        'Authorization': f"Key {getattr(django_settings, 'KHALTI_SECRET_KEY', '')}",
        'Content-Type': 'application/json',
    }

    try:
        response = http_requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            appointment.khalti_transaction_id = data.get('pidx')
            appointment.save()
            # Store ID for return
            request.session['pending_appointment_id'] = appointment.pk
            return redirect(data.get('payment_url'))
        else:
            messages.error(request, f"Khalti initiation failed: {response.text}")
            return redirect('appointment_payment', pk=appointment.pk)
    except Exception as e:
        messages.error(request, f"Payment error: {str(e)}")
        return redirect('appointment_payment', pk=appointment.pk)


@login_required
def appointment_khalti_verify(request):
    """
    KPG-2 Callback: Handles return from Khalti and verifies status using lookup API.
    """
    pidx = request.GET.get('pidx')
    if not pidx:
        messages.error(request, "Invalid payment callback.")
        return redirect('appointment_list')

   
    
    appointment_id = request.session.get('pending_appointment_id')
    if not appointment_id:
        messages.error(request, "Session expired or appointment not found.")
        return redirect('appointment_list')

    appointment = get_object_or_404(Appointment, pk=appointment_id, user=request.user)

    # Call lookup to verify
    url = f"{django_settings.KHALTI_BASE_URL}epayment/lookup/"
    payload = {"pidx": pidx}
    headers = {"Authorization": f"Key {django_settings.KHALTI_SECRET_KEY}"}

    try:
        response = http_requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'Completed':
                appointment.paid_amount = appointment.advance_amount
                appointment.payment_status = 'advance_paid'
                appointment.save()
                
                # Create a Payment record for the appointment
                from products.models import Payment
                Payment.objects.create(
                    appointment=appointment,
                    user=request.user,
                    transaction_id=f"KHALTI-APT-{pidx}",
                    payment_method='khalti',
                    amount=appointment.advance_amount,
                    status='completed',
                    payment_response=data
                )
                
                # Send email confirmation
                from django.core.mail import send_mail
                from django.conf import settings
                
                subject = f"Booking Confirmed: {appointment.pet_name}'s Grooming"
                
                context = {
                    'user_name': request.user.get_full_name() or request.user.username,
                    'appointment': appointment,
                    'service_name': appointment.get_service_display(),
                    'site_url': request.build_absolute_uri('/')[:-1]
                }
                
                html_message = render_to_string('emails/appointment_confirmation.html', context)
                plain_message = strip_tags(html_message)
                
                try:
                    send_mail(
                        subject, 
                        plain_message, 
                        settings.DEFAULT_FROM_EMAIL, 
                        [request.user.email], 
                        html_message=html_message,
                        fail_silently=True
                    )
                except Exception as e:
                    print(f"DEBUG: Appointment payment email error: {e}")
                    pass
                
                # Cleanup session
                if 'pending_appointment_id' in request.session: del request.session['pending_appointment_id']
                
                messages.success(request, f"Payment successful! Your appointment for {appointment.pet_name} is confirmed.")
                return redirect('appointment_list')
            else:
                # Payment was not completed — delete the unconfirmed appointment
                pet_name = appointment.pet_name
                appointment.delete()
                if 'pending_appointment_id' in request.session:
                    del request.session['pending_appointment_id']
                messages.warning(request, f"Payment was not completed (status: {data.get('status')}). Your booking for {pet_name} has been cancelled. Please try again.")
                return redirect('appointment_create')
        else:
            # Khalti server error — delete the unconfirmed appointment
            pet_name = appointment.pet_name
            appointment.delete()
            if 'pending_appointment_id' in request.session:
                del request.session['pending_appointment_id']
            messages.error(request, "Payment verification failed. Your booking has been cancelled. Please try again.")
            return redirect('appointment_create')
    except Exception as e:
        # Unexpected error — delete the unconfirmed appointment
        try:
            appointment.delete()
        except Exception:
            pass
        if 'pending_appointment_id' in request.session:
            del request.session['pending_appointment_id']
        messages.error(request, f"Payment error: {str(e)}. Your booking has been cancelled. Please try again.")
        return redirect('appointment_create')

@login_required
def appointment_cancel_payment(request, pk):
    """
    Called when user clicks 'Cancel Booking' on the payment page.
    Deletes the pending (unpaid) appointment so it doesn't linger.
    """
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

    # Only allow cancelling if payment has NOT been made yet
    if appointment.payment_status == 'pending_payment':
        pet_name = appointment.pet_name
        appointment.delete()
        if 'pending_appointment_id' in request.session:
            del request.session['pending_appointment_id']
        messages.info(request, f'Booking for {pet_name} cancelled. No payment was taken.')
    else:
        messages.warning(request, 'This appointment cannot be cancelled from the payment page.')

    return redirect('appointment_create')


@login_required
def appointment_update(request, pk):
    """Update an existing appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    if not request.user.is_admin_user() and appointment.user != request.user:
        messages.error(request, 'You do not have permission to edit this appointment.')
        if request.user.is_admin_user():
            return redirect('admin_appointment_list')
        return redirect('appointment_list')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            if request.user.is_admin_user():
                return redirect('admin_appointment_detail', pk=appointment.pk)
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    
    base_template = 'admin_base.html' if request.user.is_admin_user() else 'base.html'
    return render(request, 'appointments/appointment_form.html', {'form': form, 'action': 'Update', 'base_template': base_template})


@login_required
def appointment_delete(request, pk):
    """Delete an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    if not request.user.is_admin_user() and appointment.user != request.user:
        messages.error(request, 'You do not have permission to delete this appointment.')
        if request.user.is_admin_user():
            return redirect('admin_appointment_list')
        return redirect('appointment_list')
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        if request.user.is_admin_user():
            return redirect('admin_appointment_list')
        return redirect('appointment_list')
    
    base_template = 'admin_base.html' if request.user.is_admin_user() else 'base.html'
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment, 'base_template': base_template})


@login_required
def appointment_cancel(request, pk):
    """User can cancel an appointment - 24h refund rule applied."""
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

    if appointment.status in ['cancelled', 'completed']:
        messages.warning(request, f'This appointment is already {appointment.status}.')
        return redirect('appointment_detail', pk=appointment.pk)

    if request.method == 'POST':
        is_eligible = appointment.is_refund_eligible
        appointment.status = 'cancelled'
        
        if appointment.payment_status == 'advance_paid' or appointment.payment_status == 'paid':
            if is_eligible:
                import decimal
                # Deduct 50% fee (assuming advance is Rs. 10, fee is Rs. 5)
                full_advance = appointment.advance_amount
                fee = full_advance / 2
                refund_amount = full_advance - fee
                
                appointment.payment_status = 'refunded'
                # Optionally record the fee in notes or just update statuses
                messages.success(request, f'Appointment cancelled. A 50% cancellation fee (Rs. {fee}) has been deducted. Your remaining Rs. {refund_amount} will be refunded shortly.')
            else:
                messages.warning(request, 'Appointment cancelled.')
        else:
            messages.success(request, 'Appointment successfully cancelled.')
            
        appointment.save()
        return redirect('appointment_list')

    return render(request, 'appointments/appointment_confirm_cancel.html', {'appointment': appointment})


@login_required
@admin_required
def admin_appointment_pay_shop(request, pk):
    """Admin records a payment at the studio (balance or full)."""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        try:
            # We take the final total price and the actual amount paid in shop
            final_total = request.POST.get('total_price')
            shop_payment_amount = request.POST.get('payment_amount')
            payment_method = request.POST.get('payment_method', 'cash')
            
            # 1. Update the Total Price if provided
            if final_total:
                appointment.total_price = decimal.Decimal(str(final_total))
            
            # 2. Determine how much was paid at the shop
            # If admin explicitly provided an amount, use that.
            # Otherwise, use the calculated pending balance.
            if shop_payment_amount:
                amount_to_record = decimal.Decimal(str(shop_payment_amount))
            else:
                amount_to_record = appointment.pending_amount

            if amount_to_record > 0:
                # Update appointment totals
                appointment.paid_amount += amount_to_record
                
                # If we didn't have a total price yet, set it to the total paid so far
                if appointment.total_price == 0:
                    appointment.total_price = appointment.paid_amount
                
                # Update status if fully paid or just a shop payment
                if appointment.paid_amount >= appointment.total_price:
                    appointment.payment_status = 'paid'
                else:
                    appointment.payment_status = 'advance_paid' # Still partially paid
                
                appointment.save()

                # Generate a payment record
                from products.models import Payment
                from django.utils import timezone
                import uuid

                unique_suffix = f"{uuid.uuid4().hex[:4]}-{timezone.now().strftime('%y%m%d%H%M')}"
                method_display = "Online in Shop" if payment_method == 'online' else "Cash in Shop"

                Payment.objects.create(
                    appointment=appointment,
                    user=appointment.user,
                    transaction_id=f"STUDIO-{appointment.id}-{unique_suffix}",
                    payment_method=payment_method,
                    amount=amount_to_record,
                    status='completed',
                    payment_response={
                        'source': method_display,
                        'recorded_by': request.user.username,
                        'total_price_set': str(appointment.total_price),
                        'remaining_before': str(amount_to_record)
                    }
                )

                messages.success(request, f'Recorded {method_display} of Rs. {amount_to_record}. Total Paid: Rs. {appointment.paid_amount}.')
            else:
                messages.info(request, 'No payment amount to record.')
                
        except (ValueError, decimal.InvalidOperation):
            messages.error(request, 'Invalid numeric format for price or amount.')
            
        return redirect('admin_appointment_detail', pk=appointment.pk)

    return redirect('admin_appointment_detail', pk=appointment.pk)


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
            'image':       service_obj.image.url if service_obj.image else service_obj.image_url,
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
            
            # Send email confirmation
            from django.core.mail import send_mail
            from django.conf import settings
            
            subject = f"Appointment Confirmed: {appointment.pet_name}'s Grooming"
            
            context = {
                'user_name': appointment.user.get_full_name() or appointment.user.username,
                'appointment': appointment,
                'service_name': appointment.get_service_display(),
                'site_url': request.build_absolute_uri('/')[:-1]
            }
            
            html_message = render_to_string('emails/appointment_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(
                    subject, 
                    plain_message, 
                    settings.DEFAULT_FROM_EMAIL, 
                    [appointment.user.email], 
                    html_message=html_message,
                    fail_silently=True
                )
            except Exception as e:
                print(f"DEBUG: Appointment confirm email error: {e}")
                pass
                
            messages.success(request, f'Appointment for {appointment.pet_name} has been confirmed and user notified!')
        else:
            messages.warning(request, f'This appointment is already {appointment.get_status_display()}.')
        
        # Check if coming from detail page
        if request.POST.get('from_detail'):
            return redirect('admin_appointment_detail', pk=pk)
        return redirect('admin_appointment_list')
    
    return redirect('appointment_list')


@login_required
def appointment_complete(request, pk):
    """Admin or Staff can mark a confirmed appointment as completed"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions (Allow Admin or assigned Staff)
    if not request.user.is_admin_user() and not request.user.is_staff_user():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        # Can complete if confirmed or checked-in
        if appointment.status in ['confirmed', 'checked_in', 'pending']:
            appointment.status = 'completed'
            appointment.save()
            messages.success(request, f'Appointment for {appointment.pet_name} has been marked as completed!')
        elif appointment.status == 'completed':
            messages.info(request, f'Appointment for {appointment.pet_name} is already completed.')
        else:
            messages.warning(request, f'Only active appointments can be completed. Current status: {appointment.get_status_display()}.')
        
        # Determine redirection
        if request.POST.get('from_staff'):
            return redirect('staff_dashboard')
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
    
    # Metrics
    total_reviews = ServiceReview.objects.count()
    avg_rating = ServiceReview.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    approved_count = ServiceReview.objects.filter(is_approved=True).count()
    pending_count = ServiceReview.objects.filter(is_approved=False).count()
    five_star_count = ServiceReview.objects.filter(rating=5).count()
    
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
        'approved_count': approved_count,
        'pending_count': pending_count,
        'five_star_count': five_star_count,
        'service_stats': service_stats,
        'service_choices': Appointment.SERVICE_CHOICES,
        'service_filter': service_filter,
        'rating_filter': rating_filter,
    }
    
    return render(request, 'appointments/admin_service_review_list.html', context)


@login_required
@admin_required
def admin_approve_service_review(request, pk):
    """Toggle approval of a service review"""
    review = get_object_or_404(ServiceReview, pk=pk)
    review.is_approved = not review.is_approved
    review.save()
    status = "approved" if review.is_approved else "unapproved"
    messages.success(request, f'Service review has been {status}.')
    return redirect('admin_service_review_list')


@login_required
@admin_required
def admin_delete_service_review(request, pk):
    """Delete a service review"""
    review = get_object_or_404(ServiceReview, pk=pk)
    review.delete()
    messages.success(request, 'Service review deleted.')
    return redirect('admin_service_review_list')




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
        form = ServiceForm(request.POST, request.FILES)
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
        form = ServiceForm(request.POST, request.FILES, instance=service)
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
         # Block deletion if there are active appointments for this service slug
         # Appointment model uses service (choice slug) to link to types
         active_appointments = Appointment.objects.filter(
             service=service.slug, 
             status__in=['pending', 'confirmed', 'checked_in']
         )
         active_count = active_appointments.count()
         
         if active_count > 0:
             messages.error(
                 request, 
                 f'Cannot delete service "{service.name}". '
                 f'There are {active_count} active/upcoming appointment(s) booked for this service. '
                 f'Please complete or cancel those appointments first.'
             )
             return redirect('admin_service_list')

         service.delete()
         messages.success(request, f'Service "{service.name}" deleted successfully.')
         return redirect('admin_service_list')
    return render(request, 'appointments/admin_service_confirm_delete.html', {'service': service})


@login_required
@admin_required
def admin_appointment_refund(request, pk):
    """Admin manually records a refund for an appointment (e.g. cancelled booking)."""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        try:
            refund_amount = decimal.Decimal(request.POST.get('refund_amount', '0'))
            refund_method = request.POST.get('refund_method', 'cash')
            notes = request.POST.get('notes', '')
            
            if refund_amount <= 0:
                messages.error(request, 'Refund amount must be greater than zero.')
                return redirect('admin_appointment_detail', pk=pk)
            
            if refund_amount > appointment.paid_amount:
                messages.error(request, f'Refund amount cannot exceed total paid (Rs. {appointment.paid_amount}).')
                return redirect('admin_appointment_detail', pk=pk)
            
            # 1. Update appointment totals and status
            appointment.paid_amount -= refund_amount
            appointment.payment_status = 'refunded'
            # If still have some paid amount, it might remain advance_paid or similar, 
            # but usually 'refunded' status is used for the whole thing being reversed.
            appointment.save()
            
            # 2. Record the refund as a Payment object with negative amount or refunded status
            from products.models import Payment
            from django.utils import timezone
            import uuid
            
            unique_suffix = f"REF-{uuid.uuid4().hex[:4]}-{timezone.now().strftime('%y%m%d')}"
            
            Payment.objects.create(
                appointment=appointment,
                user=appointment.user,
                transaction_id=f"STUDIO-{unique_suffix}",
                payment_method=refund_method,
                amount=-refund_amount, # Negative to balance books
                status='refunded',
                payment_response={
                    'source': 'Manual Refund',
                    'recorded_by': request.user.username,
                    'notes': notes,
                    'is_manual': True
                }
            )
            
            messages.success(request, f'Succesfully recorded refund of Rs. {refund_amount} via {refund_method}. Status updated to Refunded.')
            
        except (ValueError, decimal.InvalidOperation):
            messages.error(request, 'Invalid refund amount.')
            
        return redirect('admin_appointment_detail', pk=pk)

    return redirect('admin_appointment_detail', pk=pk)


@login_required
def pet_list(request):
    """Users can see all their saved pets."""
    pets = Pet.objects.filter(user=request.user)
    return render(request, 'appointments/pet_list.html', {'pets': pets})


@login_required
@admin_required
def admin_pet_list(request):
    """Admin can see and manage all pets in the system."""
    pets = Pet.objects.all().select_related('user').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(pets, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'appointments/admin_pet_list.html', {'page_obj': page_obj})


@login_required
def pet_add(request):
    """Add a new pet profile."""
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()
            messages.success(request, f'Pet profile for {pet.name} created!')
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'appointments/pet_form.html', {'form': form, 'title': 'Add Pet'})


@login_required
def pet_edit(request, pk):
    """Edit an existing pet profile."""
    if request.user.role == 'admin':
        pet = get_object_or_404(Pet, pk=pk)
    else:
        pet = get_object_or_404(Pet, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f'{pet.name}\'s profile updated!')
            if request.user.role == 'admin':
                return redirect('admin_pet_list')
            return redirect('pet_list')
    else:
        form = PetForm(instance=pet)
    return render(request, 'appointments/pet_form.html', {'form': form, 'title': f'Edit Pet: {pet.name}'})


@login_required
def pet_delete(request, pk):
    """Delete a pet profile."""
    if request.user.role == 'admin':
        pet = get_object_or_404(Pet, pk=pk)
    else:
        pet = get_object_or_404(Pet, pk=pk, user=request.user)
        
    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Pet profile deleted.')
        if request.user.role == 'admin':
            return redirect('admin_pet_list')
        return redirect('pet_list')
    return render(request, 'appointments/pet_confirm_delete.html', {'pet': pet})
