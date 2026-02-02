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

class ServiceReview(models.Model):
    """
    Model for service reviews
    """
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_reviews')
    service = models.CharField(max_length=20, choices=Appointment.SERVICE_CHOICES)
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField()
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_reviews'
        ordering = ['-created_at']
        verbose_name = 'Service Review'
        verbose_name_plural = 'Service Reviews'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_service_display()} - {self.rating} stars"
