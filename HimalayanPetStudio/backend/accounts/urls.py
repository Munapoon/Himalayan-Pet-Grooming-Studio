from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/register/', views.user_register, name='register'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('reports/', views.reports, name='reports'),
    path('contact/', views.contact_us, name='contact_us'),
    path('contact-messages/', views.contact_messages, name='contact_messages'),
    path('contact-messages/<int:contact_id>/mark-read/', views.mark_contact_read, name='mark_contact_read'),
    path('my-contact-requests/', views.my_contact_requests, name='my_contact_requests'),
]
