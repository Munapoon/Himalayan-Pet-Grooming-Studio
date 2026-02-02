from django import forms
from .models import Appointment
from datetime import time


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet_name', 'pet_type', 'service', 'appointment_date', 'appointment_time', 'notes']
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet Name'}),
            'pet_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dog, Cat, etc.'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'min': '09:00', 'max': '18:00'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Special instructions...'}),
        }
    
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
