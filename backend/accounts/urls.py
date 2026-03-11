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
    path('contact-us/', views.contact_us, name='contact_us'), 
    path('my-contact-requests/', views.my_contact_requests, name='my_contact_requests'),
    path('admin-dashboard/contact-messages/', views.contact_messages, name='contact_messages'),
    
    # Admin Users and Reports
    path('admin-dashboard/users/', views.user_list, name='user_list'),
    path('admin-dashboard/users/<int:pk>/', views.user_detail, name='user_detail'),
    path('admin-dashboard/reports/', views.reports, name='reports'),
    
    # Password Reset & Change
    path('accounts/forgot-password/', views.forgot_password, name='forgot_password'),
    path('accounts/verify-reset-code/', views.verify_reset_code, name='verify_reset_code'),
    path('accounts/reset-password/', views.reset_password, name='reset_password'),
    path('accounts/change-password/', views.change_password, name='change_password'),
]
