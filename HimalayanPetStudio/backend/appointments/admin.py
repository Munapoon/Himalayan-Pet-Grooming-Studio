from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'user', 'service', 'appointment_date', 'appointment_time', 'status', 'created_at')
    list_filter = ('status', 'service', 'appointment_date')
    search_fields = ('pet_name', 'user__username', 'pet_type')
    date_hierarchy = 'appointment_date'
    ordering = ('-appointment_date', '-appointment_time')
