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
    path('orders/', views.order_list, name='order_list'),
    path('orders/admin/', views.admin_order_list, name='admin_order_list'),
    path('orders/admin/<str:order_number>/', views.admin_order_detail, name='admin_order_detail'),
    path('orders/admin/<str:order_number>/update-status/', views.update_order_status, name='update_order_status'),
    path('checkout/stripe/success/', views.stripe_success, name='stripe_success'),
    path('checkout/stripe/cancel/', views.stripe_cancel, name='stripe_cancel'),
    
    # Review URLs
    path('<int:pk>/review/', views.add_review, name='add_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
    path('reviews/admin/', views.admin_review_list, name='admin_review_list'),
    path('reviews/admin/<int:pk>/delete/', views.admin_delete_review, name='admin_delete_review'),
]
