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
