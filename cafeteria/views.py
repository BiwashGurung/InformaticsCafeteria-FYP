from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, FoodItem, Cart, CartItem, OrderItem, Order , LostFound , GroupOrder, GroupOrderItem , Feedback , Reply
from django.db.models import Q
from django.db import models
import uuid
import logging
import requests
import json
from django.http import JsonResponse
from datetime import datetime
#importing pytz to handle timezone(nepali time)
import pytz  

logger = logging.getLogger(__name__)

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
        messages.info(request, "Your cart is empty.")
        return render(request, 'cafeteria/cartsummary.html', {'cart': None})

    total_price = cart.total_price()
    payment_details = request.session.get('payment_details', None)
    group_code = payment_details.get('group_code', request.session.get('group_code', None)) if payment_details else request.session.get('group_code', None)

    # Check for group_code in cart items if not in session or payment_details
    try:
        if not group_code and hasattr(CartItem, 'group_code') and cart.cart_items.filter(group_code__isnull=False).exists():
            group_code = cart.cart_items.filter(group_code__isnull=False).first().group_code
    except Exception as e:
        messages.warning(request, f"Group code tracking unavailable: {str(e)}")

    return render(request, 'cafeteria/cartsummary.html', {
        'cart': cart,
        'cart_items': cart.cart_items.all(),
        'total_price': total_price,
        'group_code': group_code,
        'payment_details': payment_details
    })


@login_required
def feedback_page(request):
    query = request.GET.get('q', '').strip()
    if query:
        feedbacks = Feedback.objects.filter(
            Q(content__icontains=query) | Q(tags__icontains=query),
            is_approved=True
        ).order_by('-created_at')
    else:
        feedbacks = Feedback.objects.filter(is_approved=True).order_by('-created_at')

    top_reviewer = Feedback.objects.filter(is_approved=True).values('user__username').annotate(count=models.Count('id')).order_by('-count').first()

    if request.method == "POST":
        content = request.POST.get('content')
        image = request.FILES.get('image')
        tags = ','.join(request.POST.getlist('tags'))
        if content:
            Feedback.objects.create(user=request.user, content=content, image=image, tags=tags, is_approved=False)
            messages.success(request, "Feedback submitted for approval!")
        else:
            messages.error(request, "Content cannot be empty.")
        return redirect('feedback_page')

    context = {
        'feedbacks': feedbacks,
        'top_reviewer': top_reviewer['user__username'] if top_reviewer else None,
        'query': query
    }
    return render(request, 'cafeteria/feedback.html', context)

@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.user != feedback.user:
        messages.error(request, "You can only delete your own posts.")
        return redirect('feedback_page')
    
    if request.method == "POST":
        feedback.delete()
        messages.success(request, "Your post has been deleted successfully!")
    return redirect('feedback_page')

@login_required
def add_reply(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Reply.objects.create(feedback=feedback, user=request.user, content=content)
            messages.success(request, "Reply added!")
        else:
            messages.error(request, "Reply cannot be empty.")
    return redirect('feedback_page')

@login_required
def add_subreply(request, reply_id):
    parent_reply = get_object_or_404(Reply, id=reply_id)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Reply.objects.create(feedback=parent_reply.feedback, user=request.user, content=content, parent_reply=parent_reply)
            messages.success(request, "Reply added!")
        else:
            messages.error(request, "Reply cannot be empty.")
    return redirect('feedback_page')

@login_required
def edit_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.user != reply.user:
        messages.error(request, "You can only edit your own replies.")
        return redirect('feedback_page')
    
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            reply.content = content
            reply.save()
            messages.success(request, "Reply updated successfully!")
        else:
            messages.error(request, "Reply content cannot be empty.")
        return redirect('feedback_page')
    return redirect('feedback_page')

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.user != reply.user:
        messages.error(request, "You can only delete your own replies.")
        return redirect('feedback_page')
    
    if request.method == "POST":
        reply.delete()
        messages.success(request, "Reply deleted successfully!")
    return redirect('feedback_page')

@login_required
def react(request, feedback_id, reaction_type):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    user = request.user
    if reaction_type == 'like':
        if user in feedback.dislikes.all():
            feedback.dislikes.remove(user)
        if user in feedback.likes.all():
            feedback.likes.remove(user)
        else:
            feedback.likes.add(user)
    elif reaction_type == 'dislike':
        if user in feedback.likes.all():
            feedback.likes.remove(user)
        if user in feedback.dislikes.all():
            feedback.dislikes.remove(user)
        else:
            feedback.dislikes.add(user)
    return JsonResponse({'success': True})


@login_required
def place_order(request):
    if request.method == "POST":
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.cart_items.exists():
            messages.error(request, "Cart is empty.")
            return redirect('cartsummary')

        payment_method = request.POST.get("payment_method")
        remarks = request.POST.get("remarks", "")
        pickup_time = request.POST.get("pickup_time", None)
        dine_in_time = request.POST.get("dine_in_time", None)
        time_option = request.POST.get("time_option")  # Pickup or Dine-in
        group_code = request.POST.get("group_code", request.session.get('group_code', None))
        logger.info(f"POST data: {request.POST}, Session group_code: {request.session.get('group_code')}")

        # Validate time option selection
        if not time_option:
            messages.error(request, "Please select either Pickup Time or Dine-in Time.")
            return redirect('cartsummary')

        # Ensure mutual exclusivity
        if pickup_time and dine_in_time:
            messages.error(request, "Please select only one option: Pickup Time or Dine-in Time.")
            return redirect('cartsummary')

        # Determine selected time based on time_option
        selected_time = None
        if time_option == "pickup" and pickup_time:
            selected_time = pickup_time
        elif time_option == "dine_in" and dine_in_time:
            selected_time = dine_in_time
        else:
            messages.error(request, f"Please provide a time for the selected option ({time_option.capitalize()}).")
            return redirect('cartsummary')

        # Validate time against current time
        if selected_time:
            try:
                nepal_tz = pytz.timezone('Asia/Kathmandu')  # Adjust timezone as needed
                now = datetime.now(nepal_tz)
                time_obj = datetime.strptime(selected_time, "%H:%M").time()
                selected_datetime = datetime.combine(now.date(), time_obj)
                selected_datetime = nepal_tz.localize(selected_datetime)

                if selected_datetime < now:
                    messages.error(request, "Please don’t select a past time. Choose a time from now onwards.")
                    return redirect('cartsummary')
            except ValueError as e:
                logger.error(f"Invalid time format: {selected_time}, Error: {str(e)}")
                messages.error(request, "Invalid time format. Please use HH:MM format (e.g., 14:30).")
                return redirect('cartsummary')
            except Exception as e:
                logger.error(f"Time validation error: {str(e)}")
                messages.error(request, "An error occurred while validating the time. Please try again.")
                return redirect('cartsummary')

        if payment_method == "Online":
            payment_details = request.session.get('payment_details', None)
            if not payment_details or payment_details.get('status') != "Completed":
                messages.error(request, "Payment not completed or invalid.")
                return redirect('cartsummary')
            total_price = payment_details['amount']
            remarks = payment_details.get('remarks', remarks)
            group_code = payment_details.get('group_code', group_code)
            # Use payment_details time if available, otherwise use form input
            pickup_time = payment_details.get('pickup_time', pickup_time) if time_option == "pickup" else None
            dine_in_time = payment_details.get('dine_in_time', dine_in_time) if time_option == "dine_in" else None
        else:
            total_price = cart.total_price()

        if group_code and len(group_code) > 6:
            group_code = group_code[:6]

        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            payment_method=payment_method,
            remarks=remarks,
            pickup_time=pickup_time if time_option == "pickup" else None,
            dine_in_time=dine_in_time if time_option == "dine_in" else None,
            group_code=group_code
        )
        logger.info(f"Order created: ID={order.id}, Payment Method={payment_method}, Group Code={group_code}, Pickup Time={pickup_time}, Dine-in Time={dine_in_time}")

        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.food_item.price * item.quantity
            )
            item.delete()

        if 'group_code' in request.session:
            del request.session['group_code']
        if 'payment_details' in request.session:
            del request.session['payment_details']

        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('order_history')

    return redirect('cartsummary')

# cafeteria/views.py
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items__food_item').order_by('-order_date')
    # Queue logic for the most recent pending order
    pending_order = orders.filter(status="Pending").first()
    queue_info = {}
    if pending_order:
        # Calculate queue position (orders before this one with "Pending" or "Preparing" status)
        queue_position = Order.objects.filter(
            status__in=["Pending", "Preparing"],
            order_date__lt=pending_order.order_date
        ).count() + 1
        # Estimate wait time (5 mins per order)
        eta_minutes = queue_position * 5
        queue_info = {
            "queue_position": queue_position,
            "eta_minutes": eta_minutes,
        }
    context = {
        'orders': orders,
        'queue_info': queue_info,
    }
    return render(request, 'cafeteria/order.html', context)

# cafeteria/context_processors.py
from .models import Order

def canteen_load(request):
    pending_orders = Order.objects.filter(status__in=["Pending", "Preparing"]).count()
    if pending_orders < 10:
        return {"load_label": "Low", "load_color": "#28a745"}
    elif pending_orders < 20:
        return {"load_label": "Moderate", "load_color": "#ff9800"}
    else:
        return {"load_label": "High", "load_color": "#dc3545"}

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
    pickup_time = request.POST.get('pickup_time', '')  # Add pickup_time
    dine_in_time = request.POST.get('dine_in_time', '')  # Add dine_in_time
    group_code = request.POST.get('group_code', '')  # Add group_code
    logger.info(f"Received POST data: return_url={return_url}, amount={amount}, remarks={remarks}, pickup_time={pickup_time}, dine_in_time={dine_in_time}, group_code={group_code}")

    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cart_items.exists():
        logger.error("Cart is empty or not found")
        messages.error(request, "Cart is empty.")
        return redirect('cartsummary')

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

    # Store all fields in session
    request.session['order_remarks'] = remarks
    request.session['pickup_time'] = pickup_time
    request.session['dine_in_time'] = dine_in_time
    request.session['group_code'] = group_code if group_code else None

    payload = {
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount_in_paisa,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": purchase_order_name,
        "customer_info": {
            "name": request.user.username,
            "email": request.user.email or "cafeteria@gmail.com",
            "phone": request.user.profile.phone or "9800000000"
        }
    }
    logger.info(f"Payload sent to Khalti: {json.dumps(payload, indent=2)}")

    headers = {
        'Authorization': 'key 53a4f74df232487ba9b0b35ef76d3e39',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
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
    total_amount = request.GET.get('total_amount')
    status = request.GET.get('status')
    purchase_order_id = request.GET.get('purchase_order_id')
    
    logger.info(f"Callback params: pidx={pidx}, txn_id={txn_id}, total_amount={total_amount}, status={status}, purchase_order_id={purchase_order_id}")

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

                if not total_amount:
                    logger.error("Total amount is missing in callback")
                    messages.error(request, "Payment amount is missing.")
                    return redirect('cartsummary')

                try:
                    amount_in_npr = int(total_amount) / 100
                    logger.info(f"Converted total_amount: {total_amount} paisa to {amount_in_npr} NPR")
                except (ValueError, TypeError) as e:
                    logger.error(f"Invalid total_amount: {total_amount}, Error: {str(e)}")
                    messages.error(request, "Invalid payment amount.")
                    return redirect('cartsummary')

                # Retrieve fields from session, not POST
                group_code = request.session.get('group_code', None)
                if group_code and len(group_code) > 6:
                    group_code = group_code[:6]
                request.session['payment_details'] = {
                    'pidx': pidx,
                    'txn_id': txn_id,
                    'amount': amount_in_npr,
                    'status': 'Completed',
                    'purchase_order_id': purchase_order_id,
                    'remarks': request.session.get('order_remarks', ''),
                    'pickup_time': request.session.get('pickup_time', ''),
                    'dine_in_time': request.session.get('dine_in_time', ''),
                    'group_code': group_code
                }
                # Clean up temporary session data
                for key in ['order_remarks', 'pickup_time', 'dine_in_time', 'group_code']:
                    if key in request.session:
                        del request.session[key]

                messages.success(request, "Payment successful! Please review your cart and place the order.")
                return redirect('cartsummary')

        except requests.RequestException as e:
            logger.error(f"Payment verification failed: {str(e)}")
            messages.error(request, f"Payment verification failed: {str(e)}")
            return redirect('cartsummary')

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
    if request.method == 'POST':
        if 'create_group' in request.POST:
            # Check if the user already has an active group
            existing_active_group = GroupOrder.objects.filter(leader=request.user, is_active=True).first()
            if existing_active_group:
                messages.error(request, f"You already have an active group (Code: {existing_active_group.code}). Please close it before creating a new one.")
                return redirect('group_order_page')
            # If no active group exists, create a new one
            group = GroupOrder.objects.create(leader=request.user)
            messages.success(request, f"Group created! Share this code: {group.code}")
            return redirect('group_order_detail', group_code=group.code)

        if 'join_group' in request.POST:
            code = request.POST.get('code')
            try:
                group = GroupOrder.objects.get(code=code, is_active=True)
                return redirect('group_order_detail', group_code=group.code)
            except GroupOrder.DoesNotExist:
                messages.error(request, "Invalid or inactive group code.")
                return redirect('group_order_page')

    # Fetch active groups where the user is the leader or a participant
    active_groups = GroupOrder.objects.filter(
        Q(leader=request.user) | Q(group_items__user=request.user),
        is_active=True
    ).distinct()
    return render(request, 'cafeteria/group_order_page.html', {
        'active_groups': active_groups
    })

@login_required
def group_order_detail(request, group_code):
    try:
        group = GroupOrder.objects.get(code=group_code, is_active=True)
    except GroupOrder.DoesNotExist:
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

            # Set group_code in session
            request.session['group_code'] = group.code

            messages.success(request, f"Group order {group.code} closed. Please review and confirm your order.")
            return redirect('cartsummary')

        except Exception as e:
            messages.error(request, f"Error closing group order: {str(e)}")
            return redirect('group_order_detail', group_code=group.code)

    return render(request, 'cafeteria/group_order_detail.html', {
        'group': group,
        'food_items': food_items
    })