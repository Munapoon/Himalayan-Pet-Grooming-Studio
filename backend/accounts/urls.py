from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/register/', views.user_register, name='register'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('user-profile/remove-picture/', views.remove_profile_picture, name='remove_profile_picture'),
    path('contact-us/', views.contact_us, name='contact_us'), 
    path('my-contact-requests/', views.my_contact_requests, name='my_contact_requests'),
    path('admin-dashboard/contact-messages/', views.contact_messages, name='contact_messages'),
    
    
    path('admin-dashboard/users/', views.user_list, name='user_list'),
    path('admin-dashboard/users/<int:pk>/', views.user_detail, name='user_detail'),
    path('admin-dashboard/users/<int:pk>/update-role/', views.user_update_role, name='user_update_role'),
    path('admin-dashboard/users/<int:pk>/toggle-status/', views.user_toggle_status, name='user_toggle_status'),
    path('admin-dashboard/users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('admin-dashboard/contact-messages/<int:pk>/read/', views.mark_contact_read, name='mark_contact_read'),
    path('admin-dashboard/contact-messages/<int:pk>/delete/', views.delete_contact, name='delete_contact'),
    path('admin-dashboard/reports/', views.reports, name='reports'),
    path('admin-dashboard/reports/export-csv/', views.export_sales_csv, name='export_sales_csv'),
    path('admin-dashboard/search/', views.staff_search, name='staff_search'),
    
    
    path('accounts/forgot-password/', views.forgot_password, name='forgot_password'),
    path('accounts/verify-reset-code/', views.verify_reset_code, name='verify_reset_code'),
    path('accounts/reset-password/', views.reset_password, name='reset_password'),
    path('accounts/verify-email/', views.verify_email, name='verify_email'),
    path('accounts/change-password/', views.change_password, name='change_password'),
    path('about-us/', views.about_us, name='about_us'),
    path('legal/', views.legal, name='legal'),
]
