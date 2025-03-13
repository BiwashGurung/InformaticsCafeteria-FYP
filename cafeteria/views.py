from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, FoodItem, Cart, CartItem, OrderItem, Order

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
        
        # Checking if email already exists or not
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')
        
        


        #Creating user and profile
        user = User.objects.create_user(username=uname, email=email, password=password)
        Profile.objects.create(user=user, username=uname, email=email, phone=phone)
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'cafeteria/registration.html')

#User Login
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        next_url = request.GET.get('next')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # Updating the Profile with the session key after login
            profile, created = Profile.objects.get_or_create(user=user)
            # Storing the session key in Profile models
            profile.session_key = request.session.session_key  
            profile.expired_date = request.session.get_expiry_date()
            profile.save()

            # Handling "remember me" option
            if remember_me:
                 # adding 1week expiry time for session
                request.session.set_expiry(604800) 
            else:
                # setting the session to expire when the browser is closed if "remember me" is not checked
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
    if request.method == "POST":
        food_item = get_object_or_404(FoodItem, id=food_id)
         # Getting the quantity from the form
        quantity = int(request.POST.get("quantity", 1)) 
        
        # Getting the user's cart (Creating one if it doesn't exist)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Checking if item already exists in the cart or not
        cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

        if created:
            # Setting the quantity if it's a new item
            cart_item.quantity = quantity  
        else:
            # Increasing the quantity if item exists already
            cart_item.quantity += quantity  
        
        cart_item.save()
        messages.success(request, f"{food_item.name} added to cart successfully!")
        
    return redirect("view_cart")

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



@login_required
def cart_summary(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cart_items.exists():
        return redirect('view_cart')

    total_price = cart.total_price()
    
    return render(request, 'cafeteria/cartsummary.html', {
        'cart': cart,
        'cart_items': cart.cart_items.all(),
        'total_price': total_price
    })


@login_required
def place_order(request):
    if request.method == "POST":
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.cart_items.exists():
            return redirect('cart') 

        payment_method = request.POST.get("payment_method")
        pickup_time = request.POST.get("pickup_time")
        dine_in_time = request.POST.get("dine_in_time")
        remarks = request.POST.get("remarks", "")  # Get remarks, default to empty string

        # Create the order with remarks
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price(),
            payment_method=payment_method,
            pickup_time=pickup_time if pickup_time else None,
            dine_in_time=dine_in_time if dine_in_time else None,
            remarks=remarks  # Store remarks in the database
        )

        # Move cart items to order items
        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.food_item.price * item.quantity
            )
            item.delete()  

        return redirect('order_history') 

    return redirect('cafeteria/cartsummary.html')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'cafeteria/order.html', {'orders': orders})
