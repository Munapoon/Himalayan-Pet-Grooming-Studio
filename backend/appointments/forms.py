from django import forms
from .models import Appointment, Service, Pet
from datetime import time, timedelta, datetime
from django.utils import timezone
import json


class AppointmentForm(forms.ModelForm):
    TIME_SLOTS = [
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '01:00 PM'),
        ('14:00', '02:00 PM'),
        ('15:00', '03:00 PM'),
        ('16:00', '04:00 PM'),
        ('17:00', '05:00 PM'),
    ]

    service = forms.ChoiceField(
        choices=[], 
        widget=forms.Select(attrs={'class': 'form-select fw-bold'})
    )
    
    appointment_time = forms.ChoiceField(
        choices=TIME_SLOTS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Appointment
        fields = ['pet_name', 'pet_type', 'service', 'appointment_date', 'appointment_time', 'notes']
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet Name'}),
            'pet_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dog, Cat, etc.'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Special instructions... e.g., [Medical: Heart Issue], [Medication: Weekly injection]'
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        active_services = Service.objects.filter(is_active=True).only('slug', 'name').order_by('order')
        if active_services.exists():
            choices = [(s.slug, s.name) for s in active_services]
            self.fields['service'].choices = choices
        else:
            
            self.fields['service'].choices = Appointment.SERVICE_CHOICES
    
    def clean_appointment_time(self):
        time_str = self.cleaned_data.get('appointment_time')
        if time_str:
            
            try:
                hour, minute = map(int, time_str.split(':'))
                return time(hour, minute)
            except ValueError:
                raise forms.ValidationError("Invalid time format selected.")
        return time_str
    
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        
        if appointment_date and appointment_time:
            
            local_now = timezone.localtime()
            today = local_now.date()

            
            if appointment_date < today:
                raise forms.ValidationError('You cannot book an appointment for a past date.')
            
            if appointment_date == today:
                
                if appointment_time < local_now.time():
                    raise forms.ValidationError('Yo time already past vaiskyo. Please choose a future time.')

                
                cutoff_datetime = local_now + timedelta(minutes=30)
                
                
                if cutoff_datetime.date() > today or appointment_time < cutoff_datetime.time():
                    raise forms.ValidationError(
                        f'Appointments must be booked at least 30 minutes in advance to allow for studio preparation. '
                        f'Earliest available for today: {cutoff_datetime.strftime("%I:%M %p")}.'
                    )

            
            existing_appointments = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['pending', 'confirmed']
            )
            
            
            if self.instance and self.instance.pk:
                existing_appointments = existing_appointments.exclude(pk=self.instance.pk)
            
            MAX_CAPACITY_PER_SLOT = 1
            
            if existing_appointments.count() >= MAX_CAPACITY_PER_SLOT:
                raise forms.ValidationError('This time slot is already taken. Please choose another time or day.')

        
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
                
                parsed = json.loads(data)
                if not isinstance(parsed, list):
                    raise forms.ValidationError('Features must be a JSON list of strings.')
            except json.JSONDecodeError:
                raise forms.ValidationError('Please enter valid JSON format, e.g. ["Feature 1", "Feature 2"]')
        return data


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'pet_type', 'gender', 'breed', 'age', 'medical_notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet Name'}),
            'pet_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dog, Cat'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed (Optional)'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age in years'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Medical issues, allergies, or special care instructions...'}),
        }

