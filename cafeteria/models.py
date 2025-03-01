from django.db import models
from django.contrib.auth.models import User

#Creating a profile model to store additional information about the user in MySQL database
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=50,default='informatics.cafetera@icp.edu.np')
    

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
    price = models.DecimalField(max_digits=6, decimal_places=2)
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

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.food_item.price * self.quantity