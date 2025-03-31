from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, FoodItem, Cart, CartItem, OrderItem, Order , LostFound , GroupOrder, GroupOrderItem
from django.db.models import Q
import uuid
import logging
import requests
import json

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
    # Check if this cart contains group items
    group_code = request.session.get('group_code', None)
    if not group_code and cart.cart_items.filter(group_code__isnull=False).exists():
        group_code = cart.cart_items.filter(group_code__isnull=False).first().group_code

    return render(request, 'cafeteria/cartsummary.html', {
        'cart': cart,
        'cart_items': cart.cart_items.all(),
        'total_price': total_price,
        'group_code': group_code  
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
        remarks = request.POST.get("remarks", "")  

        group_code = request.session.get('group_code', None)
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price(),
            payment_method=payment_method,
            pickup_time=pickup_time if pickup_time else None,
            dine_in_time=dine_in_time if dine_in_time else None,
            remarks=remarks,
            group_code=group_code
        )
        if 'group_code' in request.session:
            del request.session['group_code']

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



# Khalti Payment Gateway Integration


logger = logging.getLogger(__name__)
@login_required
def initkhalti(request):
    logger.info("Entering initkhalti view")
    if request.method != "POST":
        logger.warning("Non-POST request received, redirecting to cartsummary")
        return redirect('cartsummary')

    url = "https://dev.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get('return_url')
    amount = request.POST.get('amount')
    remarks = request.POST.get('remarks', '')
    logger.info(f"Received POST data: return_url={return_url}, amount={amount}, remarks={remarks}")

    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cart_items.exists():
        logger.error("Cart is empty or not found")
        messages.error(request, "Cart is empty.")
        return redirect('view_cart')

    try:
        amount_in_paisa = int(float(amount) * 100)
        logger.info(f"Converted amount: NPR {amount} to Paisa {amount_in_paisa}")
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid amount: {amount}, Error: {str(e)}")
        messages.error(request, "Invalid amount.")
        return redirect('cartsummary')

    purchase_order_id = str(uuid.uuid4())
    purchase_order_name = f"Order-{purchase_order_id[:8]}"
    logger.info(f"Generated: purchase_order_id={purchase_order_id}, purchase_order_name={purchase_order_name}")

    request.session['order_remarks'] = remarks

    payload = {
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount_in_paisa,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": purchase_order_name,
        "customer_info": {
            "name": request.user.username,
            "email": request.user.email or "test@example.com",
            "phone": request.user.profile.phone or "9800000000"
        }
    }
    logger.info(f"Payload sent to Khalti: {json.dumps(payload, indent=2)}")

    headers = {
        'Authorization': 'key 53a4f74df232487ba9b0b35ef76d3e39',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        logger.info(f"Khalti API Response: Status={response.status_code}, Body={response.text}")
        response.raise_for_status()
        new_response = response.json()

        if 'payment_url' in new_response:
            logger.info(f"Redirecting to payment_url: {new_response['payment_url']}")
            return redirect(new_response['payment_url'])
        else:
            logger.error(f"No payment_url in response: {new_response}")
            messages.error(request, f"Failed to initiate payment: {new_response}")
            return redirect('cartsummary')

    except requests.RequestException as e:
        logger.error(f"Payment initiation failed: {str(e)}")
        messages.error(request, f"Payment initiation failed: {str(e)}")
        return redirect('cartsummary')
    

@login_required
def khalti_callback(request):
    logger.info("Entering khalti_callback view")
    
    pidx = request.GET.get('pidx')
    txn_id = request.GET.get('transaction_id') or request.GET.get('tidx') or request.GET.get('txnId')
    amount = request.GET.get('amount')
    status = request.GET.get('status')
    purchase_order_id = request.GET.get('purchase_order_id')
    
    logger.info(f"Callback params: pidx={pidx}, txn_id={txn_id}, amount={amount}, status={status}, purchase_order_id={purchase_order_id}")

    if status == "Completed":
        url = "https://dev.khalti.com/api/v2/epayment/lookup/"
        headers = {
            'Authorization': 'key 53a4f74df232487ba9b0b35ef76d3e39',
            'Content-Type': 'application/json',
        }
        payload = {"pidx": pidx}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            logger.info(f"Lookup Response: Status={response.status_code}, Body={response.text}")
            response.raise_for_status()
            payment_data = response.json()

            if payment_data.get('status') == "Completed":
                cart = Cart.objects.filter(user=request.user).first()
                if not cart or not cart.cart_items.exists():
                    logger.error("Cart is empty or not found")
                    messages.error(request, "Cart is empty.")
                    return redirect('cartsummary')

                remarks = request.session.get('order_remarks', '')
                order = Order.objects.create(
                    user=request.user,
                    total_price=int(amount) / 100,
                    payment_method="Online",
                    remarks=remarks
                )
                logger.info(f"Order created: ID={order.id}, Remarks={order.remarks}")

                for item in cart.cart_items.all():
                    OrderItem.objects.create(
                        order=order,
                        food_item=item.food_item,
                        quantity=item.quantity,
                        price=item.food_item.price * item.quantity
                    )
                    item.delete()

                if 'order_remarks' in request.session:
                    del request.session['order_remarks']

                messages.success(request, "Payment successful! Order placed.")
                return redirect('order_history')

        except requests.RequestException as e:
            logger.error(f"Payment verification failed: {str(e)}")
            messages.error(request, f"Payment verification failed: {str(e)}")

    logger.warning(f"Payment not completed: status={status}")
    messages.error(request, "Payment was not completed.")
    return redirect('cartsummary')





@login_required
def lost_found_page(request):
    approved_items = LostFound.objects.filter(status='approved')
    resolved_items = LostFound.objects.filter(status='resolved').order_by('-submitted_at')[:6]  
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        LostFound.objects.create(
            user=request.user,
            item_name=item_name,
            description=description,
            location=location,
            image=image
        )
        messages.success(request, "Your report has been submitted for approval!")
        return redirect('lost_found_page')
    return render(request, 'cafeteria/lost_found_page', {
        'approved_items': approved_items,
        'resolved_items': resolved_items
    })


@login_required
def group_order_page(request):
    if request.method == 'POST' and 'create_group' in request.POST:
        group = GroupOrder.objects.create(leader=request.user)
        messages.success(request, f"Group created! Share this code: {group.code}")
        return redirect('group_order_detail', group_code=group.code)  # Redirect directly to detail page

    if request.method == 'POST' and 'join_group' in request.POST:
        code = request.POST.get('code')
        try:
            group = GroupOrder.objects.get(code=code, is_active=True)
            return redirect('group_order_detail', group_code=group.code)
        except GroupOrder.DoesNotExist:
            messages.error(request, "Invalid or inactive group code.")
            return redirect('group_order_page')

    active_groups = GroupOrder.objects.filter(is_active=True).filter(
        Q(leader=request.user) | Q(group_items__user=request.user)
    ).distinct()
    food_items = FoodItem.objects.filter(is_in_stock=True)
    return render(request, 'cafeteria/group_order_page.html', {
        'active_groups': active_groups,
        'food_items': food_items
    })

@login_required
def group_order_detail(request, group_code):
    try:
        # Attempt to fetch the active group order
        group = GroupOrder.objects.get(code=group_code, is_active=True)
    except GroupOrder.DoesNotExist:
        # If no active group exists, redirect with a message
        messages.error(request, f"Group order {group_code} is either closed or does not exist.")
        return redirect('group_order_page')

    food_items = FoodItem.objects.filter(is_in_stock=True)

    if request.method == 'POST' and 'add_item' in request.POST:
        try:
            food_item_id = request.POST.get('food_item')
            quantity = int(request.POST.get('quantity', 1))
            food_item = get_object_or_404(FoodItem, id=food_item_id)

            GroupOrderItem.objects.create(
                group_order=group,
                user=request.user,
                food_item=food_item,
                quantity=quantity
            )
            messages.success(request, f"Added {quantity}x {food_item.name} to the group order!")
            return redirect('group_order_detail', group_code=group.code)
        except Exception as e:
            messages.error(request, f"Failed to add item: {str(e)}")
            return redirect('group_order_detail', group_code=group.code)

    if request.method == 'POST' and 'close_group' in request.POST:
        try:
            if request.user != group.leader:
                messages.error(request, "Only the group leader can close this order.")
                return redirect('group_order_detail', group_code=group.code)

            group.is_active = False
            group.save()

            leader_cart, created = Cart.objects.get_or_create(user=group.leader)
            leader_cart.cart_items.all().delete()  # Clear existing cart items

            for group_item in group.group_items.all():
                CartItem.objects.create(
                    cart=leader_cart,
                    food_item=group_item.food_item,
                    quantity=group_item.quantity,
                    username=group_item.user.username
                )

            messages.success(request, f"Group order {group.code} closed. Please review and confirm your order.")
            return redirect('cartsummary')

        except Exception as e:
            messages.error(request, f"Error closing group order: {str(e)}")
            return redirect('group_order_detail', group_code=group.code)

    return render(request, 'cafeteria/group_order_detail.html', {
        'group': group,
        'food_items': food_items
    })