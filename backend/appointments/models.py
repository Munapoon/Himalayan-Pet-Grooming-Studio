from django.db import models
from django.conf import settings
from django.utils import timezone
import json
from decimal import Decimal
from datetime import datetime


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
    image = models.ImageField(upload_to='services/', blank=True, null=True, help_text="Upload a picture for the service.")
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
        ('pending_payment', 'Pending Payment'),  # Awaiting advance — not yet confirmed
        ('unpaid', 'Unpaid'),
        ('advance_paid', 'Advance Paid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('khalti', 'Khalti'),
        ('cash', 'Cash in hand'),
        ('online', 'Online'),
    ]

    # Fixed advance amount in NPR
    ADVANCE_AMOUNT = 10

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Advance payment fields
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
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

    @property
    def is_refund_eligible(self):
        """
        Refund eligible ONLY if cancelled at least 24 hours before the appointment time.
        """
        now = timezone.now()
        
        # Combine date and time to get the appointment datetime
        # appointment_time is a time object, appointment_date is a date object
        appt_datetime = timezone.make_aware(
            datetime.combine(self.appointment_date, self.appointment_time),
            timezone.get_current_timezone()
        )
        
        time_diff = appt_datetime - now
        # Refund only if cancellation is at least 24 hours before the appointment
        return time_diff.total_seconds() >= 24 * 3600

    @property
    def pending_amount(self):
        """Calculates remaining amount if total_price is set, or uses service price as estimate."""
        import re

        target_price = self.total_price  # This is a DecimalField, always numeric
        
        # If admin hasn't set a custom total_price yet, try to get the base service price
        if target_price == 0:
            service_obj = Service.objects.filter(slug=self.service).first()
            if service_obj and service_obj.price:
                # Service.price is a CharField (e.g. "950" or "Rs. 950 - 1500")
                # Clean the string to find the first numeric value
                try:
                    # Find all numbers (including decimals) in the string
                    nums = re.findall(r"[-+]?\d*\.\d+|\d+", service_obj.price.replace(',', ''))
                    if nums:
                        target_price = Decimal(nums[0])
                except Exception:
                    target_price = Decimal('0')
        
        # Ensure we return a Decimal
        if target_price > 0:
            return max(Decimal('0'), target_price - self.paid_amount)
            
        return Decimal('0')

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
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

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
