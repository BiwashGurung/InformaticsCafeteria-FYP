from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid

# Define a function to generate the default group code
def generate_group_code():
    return uuid.uuid4().hex[:6].upper()
#Creating a profile model to store additional information about the user in MySQL database
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=50,default='informatics.cafetera@icp.edu.np')
    session_key = models.CharField(max_length=40, blank=True, null=True)
    expired_date = models.DateTimeField(blank=True, null=True)
    

    #String representation of the model 
    def __str__(self):
         # Returns the username as a string representation
        return self.user.username
    #Custom table name for profile model
    class Meta:
        db_table = 'cafeteria_users'    


# Defining the FoodItem model to store food-related details
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        validators=[MinValueValidator(1)]
    )
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='food_images/')
    is_in_stock = models.BooleanField(default=True)

    def __str__(self):
        # Returns the name of the food item as a string representation
        return self.name    
    class Meta:
        db_table = 'food_items'  




class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True) 

    def save(self, *args, **kwargs):
         #Setting  automatically username if not provided
        if not self.username: 
            self.username = self.user.username
        super().save(*args, **kwargs)

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    class Meta:
        db_table = 'cafeteria_cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)
    username = models.CharField(max_length=50, blank=True, null=True)  

    def save(self, *args, **kwargs):
        # Automatically setting the username based on the associated cart's user
        if not self.username and self.cart.user:
            self.username = self.cart.user.username
        super().save(*args, **kwargs)

    def total_price(self):
        return self.food_item.price * self.quantity  

    class Meta:
        db_table = 'cafeteria_cart_items'

class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name="order_items", on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    username = models.CharField(max_length=50, blank=True, null=True) 

    def save(self, *args, **kwargs):
        # Automatically setting the username based on the associated order's user
        if not self.username and self.order.user:
            self.username = self.order.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.food_item.name}"

    class Meta:
        db_table = "cafeteria_order_items"


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("Cash", "Payment on Delivery"),
        ("Online", "Online Payment"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Preparing", "Preparing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="Cash")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    pickup_time = models.TimeField(null=True, blank=True)
    dine_in_time = models.TimeField(null=True, blank=True)
    username = models.CharField(max_length=50, blank=True, null=True)  
    remarks = models.TextField(blank=True, null=True) 
    group_code = models.CharField(max_length=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically setting the username based on the order's user
        if not self.username and self.user:
            self.username = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    class Meta:
        db_table = "cafeteria_orders"



class LostFound(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('resolved', 'Resolved'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='lost_found/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_lost_found')

    def __str__(self):
        return f"{self.item_name} ({self.status})"

    class Meta:
        db_table = 'lost_and_found'
        verbose_name = 'Lost and Found Item'
        verbose_name_plural = 'Lost and Found Items'
        ordering = ['-submitted_at']


class GroupOrder(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_group_orders')
    code = models.CharField(max_length=6, unique=True, default=generate_group_code)  # Use the function here
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    username = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.username and self.leader:
            self.username = self.leader.username
        super().save(*args, **kwargs)

    @property
    def participants_count(self):
        # Count unique users who added items, including the leader if they contributed
        unique_users = set(item.user.id for item in self.group_items.all())
        if self.leader.id not in unique_users and self.group_items.exists():
            return len(unique_users) + 1  # Include leader if they haven't added items
        return len(unique_users) or 1  # Minimum 1 for the leader

    def __str__(self):
        return f"Group Order {self.code} by {self.leader.username}"

    class Meta:
        db_table = 'cafeteria_group_orders'

class GroupOrderItem(models.Model):
    group_order = models.ForeignKey(GroupOrder, on_delete=models.CASCADE, related_name='group_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)
    username = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.food_item.price * self.quantity
        if not self.username and self.user:
            self.username = self.user.username
        super().save(*args, **kwargs)
        self.group_order.total_price = sum(item.subtotal for item in self.group_order.group_items.all())
        self.group_order.save()

    def __str__(self):
        return f"{self.quantity}x {self.food_item.name} by {self.user.username}"

    class Meta:
        db_table = 'cafeteria_group_order_items'        