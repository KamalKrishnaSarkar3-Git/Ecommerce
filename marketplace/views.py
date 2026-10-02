from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Category, Product, Cart, CartItem, Order, OrderItem, FarmerProfile
from .forms import SignupForm, ProductForm, CheckoutForm, FarmerProfileForm, ReviewForm


def home(request):
    categories = Category.objects.all()
    featured = Product.objects.filter(is_featured=True, is_available=True)[:8]
    organic = Product.objects.filter(is_organic=True, is_available=True)[:4]
    new_arrivals = Product.objects.filter(is_available=True).order_by('-created_at')[:4]
    top_farmers = FarmerProfile.objects.filter(is_verified=True).order_by('-rating')[:4]
    return render(request, 'marketplace/home.html', {
        'categories': categories,
        'featured': featured,
        'organic': organic,
        'new_arrivals': new_arrivals,
        'top_farmers': top_farmers,
    })




def product_list(request):
    products = Product.objects.filter(is_available=True, stock__gt=0)
    categories = Category.objects.all()
    q = request.GET.get('q', '')
    cat = request.GET.get('category', '')
    organic = request.GET.get('organic', '')

    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if cat:
        products = products.filter(category__slug=cat)
    if organic == '1':
        products = products.filter(is_organic=True)

    return render(request, 'marketplace/product_list.html', {
        'products': products,
        'categories': categories,
        'q': q,
        'selected_cat': cat,
    })




@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.warning(request, "You already reviewed this product.")
        return redirect('product_detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Thanks for your review!")
        else:
            messages.error(request, "Please fix the errors.")
    return redirect('product_detail', slug=slug)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    reviews = product.reviews.select_related('user')
    user_reviewed = (
        request.user.is_authenticated and        reviews.filter(user=request.user).exists()
    )
    return render(request, 'marketplace/product_detail.html', {
        'product': product,
        'related': related,
        'reviews': reviews,
        'user_reviewed': user_reviewed,
        'review_form': ReviewForm(),
    })
    


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('is_farmer'):
                FarmerProfile.objects.create(
                    user=user,
                    farm_name=form.cleaned_data['username'],
                    location='Update your location',
                    phone='0000000000'
                )
            login(request, user)
            messages.success(request, "Welcome to FarmDirect!")
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'marketplace/signup.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'marketplace/cart.html', {'cart': cart})


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        if qty > 0:
            item.quantity = qty
            item.save()
        else:
            item.delete()
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('cart')


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.total_price()
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                item.product.stock -= item.quantity
                item.product.save()

            cart.items.all().delete()
            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'marketplace/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'marketplace/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'marketplace/my_orders.html', {'orders': orders})



# --- Seller (Farmer) Dashboard ---

@login_required
def seller_dashboard(request):
    products = Product.objects.filter(farmer=request.user)
    orders = OrderItem.objects.filter(product__farmer=request.user).select_related('order')
    total_revenue = sum(o.subtotal() for o in orders)
    return render(request, 'marketplace/seller_dashboard.html', {
        'products': products,
        'orders': orders,
        'total_revenue': total_revenue,
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'marketplace/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'marketplace/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer=request.user)
    if request.method == 'POST':
        product.delete()
        messages.info(request, "Product deleted.")
    return redirect('seller_dashboard')