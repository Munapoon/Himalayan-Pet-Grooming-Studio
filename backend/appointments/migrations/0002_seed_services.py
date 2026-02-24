import json
from django.db import migrations

DEFAULT_SERVICES = [
    {
        'slug': 'bath',
        'name': "Bath & Brush",
        'short_description': "Complete bath service with premium shampoo, conditioning, and professional blow-dry.",
        'description': "Complete bath service with premium shampoo, conditioning, blow-dry, and brush-out. Perfect for keeping your pet clean and fresh.",
        'price': "Rs. 950 - Rs. 2250",
        'duration': "45-90 minutes",
        'image_url': "https://images.unsplash.com/photo-1558788353-f76d92427f16?w=800",
        'features_json': json.dumps([
            "Premium pet shampoo & conditioner",
            "Thorough brush-out",
            "Professional blow-dry",
            "Nail trimming included",
            "Ear cleaning",
            "Paw pad moisturizing",
        ]),
        'badge': '',
        'badge_color': 'primary',
        'is_active': True,
        'order': 1,
    },
    {
        'slug': 'haircut',
        'name': "Haircut & Styling",
        'short_description': "Expert grooming & personalized styling for every breed.",
        'description': "Professional haircut and styling tailored to your pet's breed and your preferences. Our expert groomers ensure your pet looks their best.",
        'price': "Rs. 1200",
        'duration': "60-120 minutes",
        'image_url': "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=800",
        'features_json': json.dumps([
            "Breed-specific cuts",
            "Custom styling",
            "Face & feet trim",
            "Sanitary trim",
            "Full body scissoring",
            "Finishing touches",
        ]),
        'badge': '',
        'badge_color': 'primary',
        'is_active': True,
        'order': 2,
    },
    {
        'slug': 'nails',
        'name': "Nail Trimming",
        'short_description': "Quick and safe nail trimming service.",
        'description': "Professional nail trimming and filing service to keep your pet comfortable and prevent scratching.",
        'price': "Starting at Rs. 300",
        'duration': "15-30 minutes",
        'image_url': "https://images.unsplash.com/photo-1611850968574-de37a1f28b11?w=800",
        'features_json': json.dumps([
            "Precise nail trimming",
            "Smooth filing",
            "Quick check included",
            "Paw pad inspection",
            "Gentle handling",
            "Stress-free experience",
        ]),
        'badge': '',
        'badge_color': 'primary',
        'is_active': True,
        'order': 3,
    },
    {
        'slug': 'full',
        'name': "Full Grooming Package",
        'short_description': "Complete package for the ultimate pet care experience.",
        'description': "Our most comprehensive grooming package combining bath, haircut, and all finishing touches for a complete transformation.",
        'price': "Rs. 1500 - Rs. 2950",
        'duration': "2-3 hours",
        'image_url': "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800",
        'features_json': json.dumps([
            "Full bath & conditioning",
            "Complete haircut styling",
            "Nail trim & filing",
            "Teeth brushing",
            "Ear cleaning & care",
            "Paw pad trim",
            "Luxury cologne application",
            "Decorative bow or bandana",
        ]),
        'badge': 'Best Value',
        'badge_color': 'danger',
        'is_active': True,
        'order': 4,
    },
    {
        'slug': 'spa',
        'name': "Spa Treatment",
        'short_description': "Luxury spa treatment with massage and aromatherapy.",
        'description': "Luxury spa treatment for your beloved pet. Includes massage, aromatherapy, and premium grooming products for ultimate relaxation.",
        'price': "Rs. 2000 - Rs. 3500",
        'duration': "2-3 hours",
        'image_url': "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=800",
        'features_json': json.dumps([
            "Aromatherapy bath",
            "Relaxing massage",
            "Premium spa products",
            "Hot towel treatment",
            "Pawdicure service",
            "Facial treatment",
            "Calming essential oils",
            "Luxury finishing",
        ]),
        'badge': '',
        'badge_color': 'primary',
        'is_active': True,
        'order': 5,
    },
]

def seed_services(apps, schema_editor):
    Service = apps.get_model('appointments', 'Service')
    for data in DEFAULT_SERVICES:
        Service.objects.get_or_create(slug=data['slug'], defaults=data)

class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_services),
    ]
