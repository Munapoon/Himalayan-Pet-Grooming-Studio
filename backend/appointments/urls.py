from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('admin/', views.admin_appointment_list, name='admin_appointment_list'),
    path('admin/<int:pk>/', views.admin_appointment_detail, name='admin_appointment_detail'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('update/<int:pk>/', views.appointment_update, name='appointment_update'),
    path('delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),
    path('update-status/<int:pk>/', views.appointment_cancel, name='appointment_cancel'), # Reusing/Updating status logic
    path('cancel/<int:pk>/', views.appointment_cancel, name='appointment_cancel'),
    path('confirm/<int:pk>/', views.appointment_confirm, name='appointment_confirm'),
    path('complete/<int:pk>/', views.appointment_complete, name='appointment_complete'),
    path('pay-shop/<int:pk>/', views.admin_appointment_pay_shop, name='admin_appointment_pay_shop'),
    path('<int:pk>/payment/', views.appointment_payment, name='appointment_payment'),
    path('<int:pk>/khalti/initiate/', views.appointment_khalti_initiate, name='appointment_khalti_initiate'),
    path('khalti/verify/', views.appointment_khalti_verify, name='appointment_khalti_verify'),
    path('<int:pk>/cancel-payment/', views.appointment_cancel_payment, name='appointment_cancel_payment'),
    path('services/', views.service_list, name='service_list'),
    path('service/<str:service_type>/', views.service_detail, name='service_detail'),
    path('service/<str:service_type>/review/', views.add_service_review, name='add_service_review'),
    path('reviews/admin/', views.admin_service_review_list, name='admin_service_review_list'),
    
    # Service Admin CRUD
    path('admin-dashboard/services/', views.admin_service_list, name='admin_service_list'),
    path('admin-dashboard/services/add/', views.admin_service_add, name='admin_service_add'),
    path('admin-dashboard/services/edit/<int:pk>/', views.admin_service_edit, name='admin_service_edit'),
    path('admin-dashboard/services/delete/<int:pk>/', views.admin_service_delete, name='admin_service_delete'),
]
