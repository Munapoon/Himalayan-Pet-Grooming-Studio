import json
from django.db import migrations

EXTRA_SERVICES = [
    {
        'slug': 'puppy-first-bath',
        'name': "Puppy's First Bath",
        'short_description': "(For puppies less than 5 months old)",
        'description': "A gentle and positive introduction to grooming. Perfect for your puppy's first experience with specifically formulated mild shampoos and gentle handling.",
        'price': "Rs. 1600",
        'duration': "45-60 minutes",
        'image_url': "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=800",
        'features_json': json.dumps([
            "Double bath with mild puppy shampoo",
            "Conditioning & soft towel dry",
            "Nail clipping & face trim",
            "Ear & eye cleaning",
            "Sanitary area cleaning",
        ]),
        'badge': '',
        'badge_color': 'primary',
        'is_active': True,
        'order': 6,
    },
    {
        'slug': 'wash-dry',
        'name': "Wash & Dry",
        'short_description': "The perfect refresh for a clean and fresh coat.",
        'description': "Complete wash and dry service for your pet. Ideal for a quick clean-up between full grooming sessions.",
        'price': "Rs. 950 - Rs. 2250",
        'duration': "30-45 minutes",
        'image_url': "https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=800",
        'features_json': json.dumps([
            "Double bath & conditioner",
            "Blow Dry",
            "Ear & eye cleaning",
            "Light brushing",
            "Pet-safe cologne spritz",
        ]),
        'badge': '',
        'badge_color': 'primary',
        'is_active': True,
        'order': 7,
    },
    {
        'slug': 'wash-tidy',
        'name': "Wash & Tidy",
        'short_description': "A comprehensive clean with essential touch-ups.",
        'description': "A more thorough clean including essential grooming touch-ups to keep your pet looking tidy and maintained.",
        'price': "Rs. 1200 - Rs. 2600",
        'duration': "60-90 minutes",
        'image_url': "https://images.unsplash.com/photo-1597843786411-a7fa8ad44a95?w=800",
        'features_json': json.dumps([
            "Double bath & conditioner",
            "Blow dry & full body brush",
            "Nail clipping & sanitary trim",
            "Face trim & ear cleaning",
            "Eye cleaning & cologne",
        ]),
        'badge': '',
        'badge_color': 'primary',
        'is_active': True,
        'order': 8,
    },
]

def add_extra_services(apps, schema_editor):
    Service = apps.get_model('appointments', 'Service')
    for data in EXTRA_SERVICES:
        Service.objects.get_or_create(slug=data['slug'], defaults=data)

def remove_extra_services(apps, schema_editor):
    Service = apps.get_model('appointments', 'Service')
    slugs = [data['slug'] for data in EXTRA_SERVICES]
    Service.objects.filter(slug__in=slugs).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_seed_services'),
    ]

    operations = [
        migrations.RunPython(add_extra_services, reverse_code=remove_extra_services),
    ]
