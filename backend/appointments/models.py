from django.db import models
from django.conf import settings
from django.utils import timezone
import json


class Service(models.Model):
    """Dynamic grooming service model — editable from Admin Dashboard."""
    SLUG_CHOICES = [
        ('bath', 'Bath & Brush'),
        ('haircut', 'Haircut & Styling'),
        ('nails', 'Nail Trimming'),
        ('full', 'Full Grooming'),
        ('spa', 'Spa Treatment'),
    ]

    slug = models.CharField(max_length=100, unique=True,
                            help_text="Unique key that matches URL and appointment type (e.g., puppy-first-bath).")
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=255, blank=True,
                                         help_text="Short tagline shown on cards.")
    description = models.TextField(blank=True, help_text="Full description on detail page.")
    price = models.CharField(max_length=100, blank=True, help_text="e.g. Rs. 950 - Rs. 2250")
    duration = models.CharField(max_length=100, blank=True, help_text="e.g. 45-90 minutes")
    image_url = models.URLField(blank=True, help_text="External image URL for the service.")
    features_json = models.TextField(blank=True, default='[]',
                                     help_text='JSON list of feature strings, e.g. ["Bath","Nail trim"]')
    badge = models.CharField(max_length=50, blank=True,
                             help_text="Optional badge text (e.g. Best Value).")
    badge_color = models.CharField(max_length=20, default='primary',
                                   help_text="Bootstrap color: primary, danger, success, warning, info")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first).")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'services'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def features(self):
        """Return features as a Python list."""
        try:
            return json.loads(self.features_json)
        except (ValueError, TypeError):
            return []

    def set_features(self, features_list):
        """Save a Python list as JSON."""
        self.features_json = json.dumps(features_list)


class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('bath', 'Bath & Brush'),
        ('haircut', 'Haircut & Styling'),
        ('nails', 'Nail Trimming'),
        ('full', 'Full Grooming'),
        ('spa', 'Spa Treatment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('khalti', 'Khalti'),
        ('cash', 'Cash at Studio'),
    ]

    # Fixed advance amount in NPR
    ADVANCE_AMOUNT = 200

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Advance payment fields
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=200.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    khalti_transaction_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pet_name} - {self.service} ({self.appointment_date})"

    def get_service_display(self):
        """Look up the human-readable service name from the Service table."""
        svc = Service.objects.filter(slug=self.service).first()
        if svc:
            return svc.name
        # Fallback to legacy choices dict
        name = dict(self.SERVICE_CHOICES).get(self.service)
        if name:
            return name
        # Last resort: return the raw slug, prettified
        return self.service.replace('-', ' ').title()


class ServiceReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_reviews')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    service = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'service_reviews'
        unique_together = ('user', 'service')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.service} - {self.rating}"

    def get_service_display(self):
        """Look up the human-readable service name from the Service table."""
        svc = Service.objects.filter(slug=self.service).first()
        if svc:
            return svc.name
        name = dict(Appointment.SERVICE_CHOICES).get(self.service)
        if name:
            return name
        return self.service.replace('-', ' ').title()
