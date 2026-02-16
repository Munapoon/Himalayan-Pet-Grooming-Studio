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
    path('update-status/<int:pk>/', views.appointment_update_status, name='appointment_update_status'),
    path('confirm/<int:pk>/', views.appointment_confirm, name='appointment_confirm'),
    path('complete/<int:pk>/', views.appointment_complete, name='appointment_complete'),
    path('services/', views.service_list, name='service_list'),
    path('service/<str:service_type>/', views.service_detail, name='service_detail'),
    path('service/<str:service_type>/review/', views.add_service_review, name='add_service_review'),
    path('reviews/admin/', views.admin_service_review_list, name='admin_service_review_list'),
]
