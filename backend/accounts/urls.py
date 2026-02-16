from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/register/', views.user_register, name='register'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('contact/', views.home, name='contact_us'),  # Placeholder
    
    # Admin Views
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('reports/', views.reports, name='reports'),
    path('messages/', views.contact_messages, name='contact_messages'),
    
    # Emergency Reset (Added temporarily) - REMOVED
]
