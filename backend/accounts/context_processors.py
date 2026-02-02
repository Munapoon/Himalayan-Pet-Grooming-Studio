from django.conf import settings


def unread_contact_count(request):
    """
    Context processor to provide unread contact count for admin users
    """
    if request.user.is_authenticated and request.user.is_admin_user():
        from .models import Contact
        unread_count = Contact.objects.filter(is_read=False).count()
        return {'unread_contact_count': unread_count}
    return {'unread_contact_count': 0}


def khalti_config(request):
    """
    Context processor to provide Khalti configuration to all templates
    """
    return {
        'KHALTI_PUBLIC_KEY': settings.KHALTI_PUBLIC_KEY,
    }
