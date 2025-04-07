from django.contrib import admin
from .models import Profile, FoodItem , Order, Cart, CartItem, OrderItem, GroupOrder, GroupOrderItem

# Registering the Profile model to make it accessible in the Django admin panel.
admin.site.register(Profile)



# Registering the FoodItem model with additional configurations.
@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price') 
    search_fields = ('name', 'category') 
    list_filter = ('category',)  

admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'order_date', 'payment_method', 'group_code')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'id', 'group_code')
    list_editable = ('status',)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(GroupOrder)
admin.site.register(GroupOrderItem)
