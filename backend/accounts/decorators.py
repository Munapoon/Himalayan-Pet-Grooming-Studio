from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    "Decorator to restrict access to admin users only"
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin_user():
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('user_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def user_required(view_func):
    """Decorator to restrict access to regular users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_regular_user():
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
