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
]
