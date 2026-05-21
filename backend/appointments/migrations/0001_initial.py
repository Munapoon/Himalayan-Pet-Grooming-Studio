

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(max_length=100)),
                ('pet_type', models.CharField(max_length=100)),
                ('service', models.CharField(choices=[('bath', 'Bath & Brush'), ('haircut', 'Haircut & Styling'), ('nails', 'Nail Trimming'), ('full', 'Full Grooming'), ('spa', 'Spa Treatment')], max_length=20)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'appointments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(choices=[('bath', 'Bath & Brush'), ('haircut', 'Haircut & Styling'), ('nails', 'Nail Trimming'), ('full', 'Full Grooming'), ('spa', 'Spa Treatment')], help_text='Unique key that matches URL and appointment type.', max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('short_description', models.CharField(blank=True, help_text='Short tagline shown on cards.', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Full description on detail page.')),
                ('price', models.CharField(blank=True, help_text='e.g. Rs. 950 - Rs. 2250', max_length=100)),
                ('duration', models.CharField(blank=True, help_text='e.g. 45-90 minutes', max_length=100)),
                ('image_url', models.URLField(blank=True, help_text='External image URL for the service.')),
                ('features_json', models.TextField(blank=True, default='[]', help_text='JSON list of feature strings, e.g. ["Bath","Nail trim"]')),
                ('badge', models.CharField(blank=True, help_text='Optional badge text (e.g. Best Value).', max_length=50)),
                ('badge_color', models.CharField(default='primary', help_text='Bootstrap color: primary, danger, success, warning, info', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order (lower = first).')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'services',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ServiceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(choices=[('bath', 'Bath & Brush'), ('haircut', 'Haircut & Styling'), ('nails', 'Nail Trimming'), ('full', 'Full Grooming'), ('spa', 'Spa Treatment')], max_length=20)),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Star'), (3, '3 Star'), (4, '4 Star'), (5, '5 Star')])),
                ('review', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='appointments.appointment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'service_reviews',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'service')},
            },
        ),
    ]
