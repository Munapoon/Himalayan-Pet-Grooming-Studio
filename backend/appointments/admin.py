from django.contrib import admin
from .models import Service, Appointment, ServiceReview





@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'duration', 'is_active', 'order')
    list_filter = ('is_active', 'slug')
    search_fields = ('name', 'description', 'slug')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('slug', 'name', 'short_description', 'description')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration')
        }),
        ('Media & Display', {
            'fields': ('image_url', 'badge', 'badge_color', 'order', 'is_active')
        }),
        ('Features (JSON list)', {
            'fields': ('features_json',),
            'description': 'Enter a JSON list of string features, e.g. ["Bath","Nail trim","Ear clean"]'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )





@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'pet_type', 'service', 'appointment_date',
                    'appointment_time', 'status', 'user', 'created_at')
    list_filter = ('status', 'service', 'appointment_date')
    search_fields = ('pet_name', 'pet_type', 'user__username', 'user__email')
    list_editable = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'appointment_date'

    fieldsets = (
        ('Pet Details', {
            'fields': ('pet_name', 'pet_type')
        }),
        ('Appointment', {
            'fields': ('user', 'service', 'appointment_date', 'appointment_time', 'notes')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )





@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'rating', 'created_at')
    list_filter = ('service', 'rating')
    search_fields = ('user__username', 'review')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
