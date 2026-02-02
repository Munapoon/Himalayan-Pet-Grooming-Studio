from .models import Cart


def cart_count(request):
    """Add cart item count to context"""
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
        return {'cart_count': count}
    return {'cart_count': 0}
