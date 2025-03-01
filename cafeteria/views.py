from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, FoodItem ,Cart ,CartItem


#Rendering the homepage 
def HomePage(request):
    return render(request, 'cafeteria/index.html')

# handeling the signup process when the user submits the registration form
def SignupPage(request):
    #Extracting thhe user input data from the form
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        #Cheking whether the password matches or not
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        # Checking wether the  username already exists or not
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        #Creating the user and associated profile
        user = User.objects.create_user(username=uname, email=email, password=password)
        Profile.objects.create(user=user,username=uname,email=email, phone=phone)
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')
    #redering the registration page
    return render(request, 'cafeteria/registration.html')

#Handeling the user's login process
def LoginPage(request):
    if request.method == 'POST':
        #Extracting login credentials from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        #Authenticating the user's with their provided credentials
        user = authenticate(request, username=username, password=password)
        #Checking id the user us authenticated 
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # Handling session expiration based on 'remember me'
            if remember_me:
                # 1 week session expiry
                request.session.set_expiry(604800)  
            else:
                # Session expires when the browser is closed
                request.session.set_expiry(0) 

            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'cafeteria/login.html')

def LogoutPage(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


def CollegePage(request):
    return render(request, 'cafeteria/college.html')    

def AboutUsPage(request):
    return render(request, 'cafeteria/aboutus.html')

def ContactUsPage(request):
    return render(request, 'cafeteria/contactus.html')

def OrderOnline(request):
    return render(request, 'cafeteria/orderonline.html')

#Displaying the food items for a specific category
def food_list(request, category):
    #Fetching the food items from database based on category
    food_items = FoodItem.objects.filter(category=category)
    #Rendering the food list page with food items
    return render(request, 'cafeteria/food_list.html', {'food_items': food_items, 'category': category})    



#Displaying Cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    total_price = cart.total_price()
    return render(request, 'cafeteria/cart.html', {'cart_items': cart_items, 'total_price': total_price})

#Adding Item to Cart
@login_required
def add_to_cart(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    #Checking if item is already in cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

#Updating Cart Item Quantity
@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            # Removing item if quantity is 0
            cart_item.delete()  
    return redirect('view_cart')

#Removing Item from Cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')

# Clearing Cart
@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.cart_items.all().delete()
    return redirect('view_cart')