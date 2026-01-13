from django.db import models
from accounts.models import User


class Appointment(models.Model):
    """
    Model for pet grooming appointments
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    SERVICE_CHOICES = [
        ('bath', 'Bath & Brush'),
        ('haircut', 'Haircut & Styling'),
        ('nails', 'Nail Trimming'),
        ('full', 'Full Grooming Package'),
        ('spa', 'Spa Treatment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=50)  # Dog, Cat, etc.
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_date', '-appointment_time']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
    
    def __str__(self):
        return f"{self.pet_name} - {self.get_service_display()} on {self.appointment_date}"
