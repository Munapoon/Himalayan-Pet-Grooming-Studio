from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import admin_required
from .models import ProductCategory, Product, Cart, Sale, Order, OrderItem
from .forms import ProductCategoryForm, ProductForm


# Product Category Views
@login_required
@admin_required
def category_list(request):
    from django.core.paginator import Paginator
    
    categories = ProductCategory.objects.all().order_by('-created_at')
    
    # Pagination - 10 categories per page
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/category_list.html', {'page_obj': page_obj})


@login_required
@admin_required
def category_create(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('products:category_list')
    else:
        form = ProductCategoryForm()
    return render(request, 'products/category_form.html', {'form': form, 'action': 'Create'})


@login_required
@admin_required
def category_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('products:category_list')
    else:
        form = ProductCategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'form': form, 'action': 'Update', 'category': category})


@login_required
@admin_required
def category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('products:category_list')
    return render(request, 'products/category_confirm_delete.html', {'category': category})


# Product Views
def product_list(request):
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    # Get search query, category filter, and sort option
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'newest')
    
    if request.user.is_authenticated and request.user.is_admin_user():
        products = Product.objects.all()
        # Note: If product_list_admin.html doesn't exist, we use product_list.html
        template_name = 'products/product_list.html'
    else:
        products = Product.objects.filter(is_active=True)
        template_name = 'products/product_list.html'
    
    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Apply category filter
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Apply sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating', '-created_at')
    else:  # newest (default)
        products = products.order_by('-created_at')
    
    # Pagination - 10 products per page
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = ProductCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_id': category_id,
        'sort_by': sort_by,
        'categories': categories,
    }
    
    return render(request, template_name, context)


@login_required
@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Create'})


def product_detail(request, pk):
    from .models import Review, Sale
    product = get_object_or_404(Product, pk=pk)
    
    # Check if user has purchased this product
    has_purchased = False
    if request.user.is_authenticated and not request.user.is_admin_user():
        has_purchased = Sale.objects.filter(
            customer=request.user,
            product=product
        ).exists()
    
    # Get user's existing review if any
    user_review = None
    if request.user.is_authenticated and not request.user.is_admin_user():
        user_review = Review.objects.filter(product=product, user=request.user).first()
    
    # Get all reviews for this product
    reviews = Review.objects.filter(product=product).select_related('user')
    
    context = {
        'product': product,
        'has_purchased': has_purchased,
        'user_review': user_review,
        'reviews': reviews,
    }
    
    if request.user.is_authenticated and request.user.is_admin_user():
        template_name = 'products/product_detail_admin.html'
    else:
        template_name = 'products/product_detail.html'
    return render(request, template_name, context)


@login_required
@admin_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Update', 'product': product})


@login_required
@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


# Cart Views
@login_required
def cart_view(request):
    """View cart items"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    total = sum(item.subtotal for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'products/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    
    if not product.in_stock:
        messages.error(request, 'This product is currently out of stock.')
        return redirect('products:product_detail', pk=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    redirect_to = request.POST.get('redirect_to', 'cart')
    
    # Check if item already in cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Update quantity if item already exists
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Updated {product.name} quantity in cart.')
    else:
        messages.success(request, f'{product.name} added to cart successfully!')
    
    # Redirect based on the redirect_to parameter
    if redirect_to == 'product':
        return redirect('products:product_detail', pk=product_id)
    else:
        return redirect('products:cart')


@login_required
def update_cart(request, cart_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            if quantity <= cart_item.product.stock_quantity:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated successfully!')
            else:
                messages.error(request, f'Only {cart_item.product.stock_quantity} items available in stock.')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    
    return redirect('products:cart')


@login_required
def remove_from_cart(request, cart_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('products:cart')


@login_required
def clear_cart(request):
    """Clear all items from cart"""
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, 'Cart cleared successfully!')
    return redirect('products:cart')


@login_required
def add_review(request, pk):
    """Add or update a product review"""
    from .models import Review, Sale
    from .forms import ReviewForm
    
    product = get_object_or_404(Product, pk=pk)
    
    # Check if user has purchased this product
    has_purchased = Sale.objects.filter(
        customer=request.user,
        product=product
    ).exists()
    
    if not has_purchased:
        messages.error(request, 'You can only review products you have purchased.')
        return redirect('products:product_detail', pk=pk)
    
    # Check if user already has a review
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    
    if request.method == 'POST':
        if existing_review:
            form = ReviewForm(request.POST, instance=existing_review)
        else:
            form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('products:product_detail', pk=pk)
    else:
        if existing_review:
            form = ReviewForm(instance=existing_review)
        else:
            form = ReviewForm()
    
    context = {
        'form': form,
        'product': product,
        'existing_review': existing_review,
    }
    return render(request, 'products/review_form.html', context)


@login_required
def delete_review(request, pk):
    """Delete a product review"""
    from .models import Review
    
    review = get_object_or_404(Review, pk=pk)
    product_id = review.product.id
    
    # Check if user owns this review
    if review.user != request.user:
        messages.error(request, 'You can only delete your own reviews.')
        return redirect('products:product_detail', pk=product_id)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('products:product_detail', pk=product_id)
    
    return render(request, 'products/review_confirm_delete.html', {'review': review})


# Checkout & Order Views
@login_required
def checkout(request):
    """Checkout page with payment options"""
    from .models import Order, OrderItem
    
    # Get selected item IDs from POST request
    selected_item_ids = request.POST.getlist('selected_items')
    
    if selected_item_ids:
        # Filter cart items by selected IDs
        cart_items = Cart.objects.filter(
            user=request.user, 
            id__in=selected_item_ids
        ).select_related('product')
        # Store selected IDs in session for later use
        request.session['selected_cart_items'] = selected_item_ids
    elif 'selected_cart_items' in request.session:
        # Use stored selection from session
        cart_items = Cart.objects.filter(
            user=request.user,
            id__in=request.session['selected_cart_items']
        ).select_related('product')
    else:
        # No selection - use all cart items
        cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty or no items selected.')
        return redirect('products:cart')
    
    # Check stock availability
    for item in cart_items:
        if item.quantity > item.product.stock_quantity:
            messages.error(request, f'{item.product.name} has insufficient stock.')
            return redirect('products:cart')
    
    total = sum(item.subtotal for item in cart_items)
    
    if request.method == 'POST' and 'payment_method' in request.POST:
        payment_method = request.POST.get('payment_method')
        shipping_address = request.POST.get('shipping_address')
        phone_number = request.POST.get('phone_number')
        notes = request.POST.get('notes', '')
        
        if not shipping_address or not phone_number:
            messages.error(request, 'Please provide shipping address and phone number.')
            return render(request, 'products/checkout.html', {
                'cart_items': cart_items,
                'total': total,
            })
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            payment_method=payment_method,
            shipping_address=shipping_address,
            phone_number=phone_number,
            notes=notes,
        )
        
        # Create order items and update stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,
            )
            
            # Update product stock
            item.product.stock_quantity -= item.quantity
            item.product.save()
            
            # Create Sale record for purchase verification (for reviews)
            Sale.objects.create(
                product=item.product,
                customer=request.user,
                quantity=item.quantity,
                unit_price=item.product.price,
                payment_method='online' if payment_method == 'khalti' else 'cash',
            )
        
        # Clear only the selected cart items
        cart_items.delete()
        
        # Clear session data
        if 'selected_cart_items' in request.session:
            del request.session['selected_cart_items']
        
        if payment_method == 'cod':
            # Cash on Delivery - Order is pending
            order.payment_status = 'pending'
            order.save()
            messages.success(request, f'Order placed successfully! Order Number: {order.order_number}')
            return redirect('products:order_detail', order_number=order.order_number)
        
        elif payment_method == 'khalti':
            # Khalti payment - Store order in session and redirect to Khalti verification
            order.payment_status = 'pending'
            order.save()
            
            # Store order number in session for verification
            request.session['pending_order'] = order.order_number
            
            # Return checkout page with Khalti payment widget
            context = {
                'cart_items': cart_items,
                'total': total,
                'order': order,
                'show_khalti': True,
            }
            return render(request, 'products/checkout.html', context)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'products/checkout.html', context)


@login_required
def order_detail(request, order_number):
    """View order details"""
    from .models import Order
    
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'products/order_detail.html', context)


@login_required
def order_list(request):
    """View all user orders"""
    from .models import Order
    
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    
    context = {
        'orders': orders,
    }
    return render(request, 'products/order_list.html', context)


@login_required
def khalti_verify(request):
    """Khalti payment verification callback"""
    import requests
    from django.conf import settings
    
    if request.method == 'POST':
        token = request.POST.get('token')
        amount = request.POST.get('amount')
        
        # Verify payment with Khalti
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}"
        }
        
        try:
            response = requests.post(url, payload, headers=headers)
            
            if response.status_code == 200:
                # Payment verified successfully
                order_number = request.session.get('pending_order')
                if order_number:
                    from .models import Order, Payment
                    order = Order.objects.get(order_number=order_number)
                    order.payment_status = 'paid'
                    order.payment_method = 'khalti'
                    order.save()
                    
                    # Create payment record
                    payment_data = response.json()
                    Payment.objects.create(
                        order=order,
                        user=request.user,
                        transaction_id=payment_data.get('idx', token),
                        payment_method='khalti',
                        amount=order.total_amount,
                        status='completed',
                        payment_response=payment_data
                    )
                    
                    # Clear session
                    del request.session['pending_order']
                    
                    messages.success(request, f'Payment successful! Order Number: {order.order_number}')
                    return redirect('products:order_detail', order_number=order.order_number)
            else:
                messages.error(request, 'Payment verification failed. Please contact support.')
                return redirect('products:cart')
        except Exception as e:
            messages.error(request, f'Payment verification error: {str(e)}')
            return redirect('products:cart')
    
    return redirect('products:cart')


# Admin Order Management Views
@login_required
@admin_required
def admin_order_list(request):
    """Admin view to list all orders"""
    from django.db.models import Q
    from django.core.paginator import Paginator
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    payment_status_filter = request.GET.get('payment_status', '')
    payment_method_filter = request.GET.get('payment_method', '')
    search_query = request.GET.get('search', '')
    
    orders = Order.objects.all().select_related('user').prefetch_related('items__product').order_by('-created_at')
    
    # Apply filters
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if payment_status_filter:
        orders = orders.filter(payment_status=payment_status_filter)
    
    if payment_method_filter:
        orders = orders.filter(payment_method=payment_method_filter)
    
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
    
    # Pagination - 10 orders per page
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics for all filtered orders (not just current page)
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    total_revenue = sum(order.total_amount for order in orders.filter(payment_status='paid'))
    pending_revenue = sum(order.total_amount for order in orders.filter(payment_method='cod', status__in=['pending', 'processing']))
    completed_orders = orders.filter(status='completed').count()
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'payment_status_filter': payment_status_filter,
        'payment_method_filter': payment_method_filter,
        'search_query': search_query,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'pending_revenue': pending_revenue,
        'completed_orders': completed_orders,
    }
    return render(request, 'products/admin_order_list.html', context)


@login_required
@admin_required
def admin_order_detail(request, order_number):
    """Admin view to see order details"""
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order,
    }
    return render(request, 'products/admin_order_detail.html', context)


@login_required
@admin_required
def update_order_status(request, order_number):
    """Update order status and payment status"""
    order = get_object_or_404(Order, order_number=order_number)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_payment_status = request.POST.get('payment_status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
        
        if new_payment_status in dict(Order.PAYMENT_STATUS_CHOICES):
            order.payment_status = new_payment_status
        
        order.save()
        messages.success(request, f'Order #{order.order_number} updated successfully!')
        return redirect('products:admin_order_detail', order_number=order.order_number)
    
    return redirect('products:admin_order_list')


# Admin Review Management Views
@login_required
@admin_required
def admin_review_list(request):
    """Admin view to list all product reviews"""
    from .models import Review
    from django.db.models import Q
    from django.core.paginator import Paginator
    
    # Get filter parameters
    rating_filter = request.GET.get('rating', '')
    product_filter = request.GET.get('product', '')
    search_query = request.GET.get('search', '')
    
    reviews = Review.objects.all().select_related('product', 'user').order_by('-created_at')
    
    # Apply filters
    if rating_filter:
        reviews = reviews.filter(rating=rating_filter)
    
    if product_filter:
        reviews = reviews.filter(product_id=product_filter)
    
    if search_query:
        reviews = reviews.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(product__name__icontains=search_query) |
            Q(comment__icontains=search_query)
        )
    
    # Pagination - 10 reviews per page
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all products for filter dropdown
    products = Product.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'rating_filter': rating_filter,
        'product_filter': product_filter,
        'search_query': search_query,
        'products': products,
    }
    return render(request, 'products/admin_review_list.html', context)


@login_required
@admin_required
def admin_delete_review(request, pk):
    """Admin view to delete a review"""
    from .models import Review
    
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'POST':
        product_name = review.product.name
        user_name = review.user.get_full_name() or review.user.username
        review.delete()
        messages.success(request, f'Review by {user_name} for {product_name} has been deleted.')
        return redirect('products:admin_review_list')
    
    return render(request, 'products/admin_review_confirm_delete.html', {'review': review})


# Payment Views
@login_required
def user_payment_list(request):
    """User view to see their payment history"""
    from .models import Payment
    from django.core.paginator import Paginator
    
    payments = Payment.objects.filter(user=request.user).select_related('order')
    
    # Pagination
    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_payments': payments.count(),
        'total_amount': sum(p.amount for p in payments if p.status == 'completed'),
    }
    return render(request, 'products/user_payment_list.html', context)


@login_required
@admin_required
def admin_payment_list(request):
    """Admin view to see all payments"""
    from .models import Payment
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    payment_method_filter = request.GET.get('payment_method', '')
    search_query = request.GET.get('search', '')
    
    # Base queryset
    payments = Payment.objects.all().select_related('order', 'user')
    
    # Apply filters
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    if payment_method_filter:
        payments = payments.filter(payment_method=payment_method_filter)
    
    if search_query:
        payments = payments.filter(
            Q(transaction_id__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(order__order_number__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(payments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    all_payments = Payment.objects.all()
    completed_payments = all_payments.filter(status='completed')
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'payment_method_filter': payment_method_filter,
        'search_query': search_query,
        'total_payments': all_payments.count(),
        'completed_payments': completed_payments.count(),
        'total_revenue': sum(p.amount for p in completed_payments),
        'status_choices': Payment.STATUS_CHOICES,
        'payment_method_choices': Payment.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'products/admin_payment_list.html', context)


@login_required
@admin_required
def admin_payment_detail(request, pk):
    """Admin view to see payment details"""
    from .models import Payment
    
    payment = get_object_or_404(Payment.objects.select_related('order', 'user'), pk=pk)
    
    context = {
        'payment': payment,
    }
    return render(request, 'products/admin_payment_detail.html', context)
