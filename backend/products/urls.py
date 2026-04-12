from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Product URLs
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    # Checkout & Order URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('order/<str:order_number>/cancel/', views.order_cancel, name='order_cancel'),
    path('order/<str:order_number>/edit/', views.order_edit, name='order_edit'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/admin/', views.admin_order_list, name='admin_order_list'),
    path('orders/admin/<str:order_number>/', views.admin_order_detail, name='admin_order_detail'),
    path('orders/admin/<str:order_number>/update-status/', views.update_order_status, name='update_order_status'),
    path('orders/admin/<str:order_number>/refund/', views.admin_order_refund, name='admin_order_refund'),
    path('checkout/khalti/verify/', views.khalti_verify, name='khalti_verify'),
    
    # Review URLs
    path('<int:pk>/review/', views.add_review, name='add_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
    path('reviews/admin/', views.admin_review_list, name='admin_review_list'),
    path('reviews/admin/<int:pk>/delete/', views.admin_delete_review, name='admin_delete_review'),
    path('reviews/admin/<int:pk>/approve/', views.admin_approve_review, name='admin_approve_review'),
    
    # Payment URLs
    path('payments/', views.user_payment_list, name='user_payment_list'),
    path('payments/admin/', views.admin_payment_list, name='admin_payment_list'),
    path('payments/admin/<int:pk>/', views.admin_payment_detail, name='admin_payment_detail'),
    
    # Export URLs
    path('export/orders/excel/', views.export_orders_excel, name='export_orders_excel'),
    path('export/orders/csv/', views.export_orders_csv, name='export_orders_csv'),
    path('export/payments/excel/', views.export_payments_excel, name='export_payments_excel'),
    path('export/payments/csv/', views.export_payments_csv, name='export_payments_csv'),
    path('export/sales/csv/', views.export_sales_csv, name='export_sales_csv'),

]
