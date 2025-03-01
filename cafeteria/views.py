from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, FoodItem, Cart, CartItem

# Home Page
def HomePage(request):
    return render(request, 'cafeteria/index.html')

# User Signup
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Checking if passwords match or not 
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        # Checking if username already exists or not 
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        #Creating user and profile
        user = User.objects.create_user(username=uname, email=email, password=password)
        Profile.objects.create(user=user, username=uname, email=email, phone=phone)
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'cafeteria/registration.html')

# User Login
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        # Getting the next URL if it exists
        next_url = request.GET.get('next')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # Handling "remember me"
            if remember_me:
                # 1 week(7days) session expiry
                request.session.set_expiry(604800)  
            else:
                # It will expires when browser closes
                request.session.set_expiry(0)  

            # Redirecting to the previous page or home if no next URL is provided
            return redirect(next_url) if next_url else redirect('home')

        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'cafeteria/login.html')


# User Logout
def LogoutPage(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

# Other Static Pages
def CollegePage(request):
    return render(request, 'cafeteria/college.html')

def AboutUsPage(request):
    return render(request, 'cafeteria/aboutus.html')

def ContactUsPage(request):
    return render(request, 'cafeteria/contactus.html')

def OrderOnline(request):
    return render(request, 'cafeteria/orderonline.html')

# Displaying Food Items by its Category
def food_list(request, category):
    food_items = FoodItem.objects.filter(category=category)
    return render(request, 'cafeteria/food_list.html', {'food_items': food_items, 'category': category})

# View Cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
     # Optimizing Query to fetch related food items
    cart_items = cart.cart_items.select_related('food_item') 
    total_price = cart.total_price()
    return render(request, 'cafeteria/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Add Item to Cart
@login_required
def add_to_cart(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    
    if not food_item.is_in_stock:
        messages.error(request, 'This item is out of stock.')
        return redirect('food_list', category=food_item.category)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{food_item.name} added to cart.")
    return redirect('view_cart')

# Update Cart Item Quantity
@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))
        
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
        else:
            cart_item.delete()
            messages.info(request, "Item removed from cart.")

    return redirect('view_cart')

# Remove Item from Cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')

# Clear Cart
@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.cart_items.all().delete()
    messages.success(request, "Cart cleared successfully.")
    return redirect('view_cart')
