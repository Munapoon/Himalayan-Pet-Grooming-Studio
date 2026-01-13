from .models import Contact


def unread_contact_count(request):
    """Add unread contact message count to context"""
    if request.user.is_authenticated and request.user.is_admin():
        unread_count = Contact.objects.filter(is_read=False).count()
        return {'unread_count': unread_count}
    return {'unread_count': 0}
