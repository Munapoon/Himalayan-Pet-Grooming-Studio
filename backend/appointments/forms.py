from django import forms
from .models import Appointment, Service
from datetime import time, timedelta, datetime
from django.utils import timezone
import json


class AppointmentForm(forms.ModelForm):
    service = forms.ChoiceField(
        choices=[], 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['pet_name', 'pet_type', 'service', 'appointment_date', 'appointment_time', 'notes']
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet Name'}),
            'pet_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dog, Cat, etc.'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'min': '09:00', 'max': '18:00'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Special instructions... e.g., [Medical: Heart Issue], [Medication: Weekly injection]'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set service choices from Service model
        active_services = Service.objects.filter(is_active=True).only('slug', 'name').order_by('order')
        if active_services.exists():
            choices = [(s.slug, s.name) for s in active_services]
            self.fields['service'].choices = choices
        else:
            # Fallback to model choices if DB is empty
            self.fields['service'].choices = Appointment.SERVICE_CHOICES
    
    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        
        # Check if time is between 9 AM and 6 PM
        if appointment_time:
            if appointment_time < time(9, 0) or appointment_time >= time(18, 0):
                raise forms.ValidationError('Appointments are only available between 9:00 AM and 6:00 PM.')
        
        return appointment_time
    
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        
        if appointment_date and appointment_time:
            # Get current local time (naive, stripped of tzinfo for comparison with form's naive time)
            local_now = timezone.localtime()
            today = local_now.date()

            # Check if appointment is in the past or too soon
            if appointment_date < today:
                raise forms.ValidationError('You cannot book an appointment for a past date.')
            
            if appointment_date == today:
                # Enforce 30-minute advance booking for today's appointments
                cutoff_datetime = local_now + timedelta(minutes=30)
                
                # If 30 minutes from now is already past today's operating hours (handled by clean_appointment_time)
                # or if it rolls to tomorrow, just show a general "too soon" message.
                if cutoff_datetime.date() > today or appointment_time < cutoff_datetime.time():
                    raise forms.ValidationError(
                        f'Appointments must be booked at least 30 minutes in advance to allow for studio preparation. '
                        f'Earliest available for today: {cutoff_datetime.strftime("%I:%M %p")}.'
                    )

            # Check if slot is already booked
            existing_appointment = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['pending', 'confirmed']
            )
            
            # Exclude current appointment if updating
            if self.instance and self.instance.pk:
                existing_appointment = existing_appointment.exclude(pk=self.instance.pk)
            
            if existing_appointment.exists():
                raise forms.ValidationError(
                    f'This time slot is already booked. Please choose a different date or time.'
                )
        
        return cleaned_data


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'name', 'slug', 'short_description', 'description', 
            'price', 'duration', 'image_url', 'image', 'features_json', 
            'badge', 'badge_color', 'is_active', 'order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. bath-brush'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief tagline...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed description...'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Rs. 1500'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 60-90 min'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'features_json': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': '["Feature 1", "Feature 2"]'
            }),
            'badge': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Popular'}),
            'badge_color': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('primary', 'Primary (Blue)'),
                ('success', 'Success (Green)'),
                ('danger', 'Danger (Red)'),
                ('warning', 'Warning (Yellow)'),
                ('info', 'Info (Cyan)'),
                ('dark', 'Dark'),
            ]),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_features_json(self):
        data = self.cleaned_data.get('features_json')
        if data:
            try:
                # Validate that it's a valid JSON list
                parsed = json.loads(data)
                if not isinstance(parsed, list):
                    raise forms.ValidationError('Features must be a JSON list of strings.')
            except json.JSONDecodeError:
                raise forms.ValidationError('Please enter valid JSON format, e.g. ["Feature 1", "Feature 2"]')
        return data

