from django.contrib import admin
from .models import Appointment, ServiceReview


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'user', 'service', 'appointment_date', 'appointment_time', 'status', 'created_at')
    list_filter = ('status', 'service', 'appointment_date')
    search_fields = ('pet_name', 'user__username', 'pet_type')
    date_hierarchy = 'appointment_date'
    ordering = ('-appointment_date', '-appointment_time')


@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'rating', 'appointment', 'created_at')
    list_filter = ('service', 'rating', 'created_at')
    search_fields = ('user__username', 'review')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
