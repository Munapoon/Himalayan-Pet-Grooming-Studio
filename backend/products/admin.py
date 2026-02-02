from django.contrib import admin
from .models import ProductCategory, Product, Sale, Cart, Review, Order, OrderItem, Payment


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    list_per_page = 20


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer', 'quantity', 'total_amount', 'payment_method', 'sale_date']
    list_filter = ['payment_method', 'sale_date']
    search_fields = ['product__name', 'customer__username']
    list_per_page = 20


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'payment_method', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_per_page = 20


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'subtotal', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__name']
    list_per_page = 20


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'order', 'payment_method', 'amount', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['transaction_id', 'user__username', 'user__email', 'order__order_number']
    readonly_fields = ['transaction_id', 'payment_response', 'created_at', 'updated_at']
    list_per_page = 20
