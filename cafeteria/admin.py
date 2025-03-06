from django.contrib import admin
from .models import Profile, FoodItem , Order

# Registering the Profile model to make it accessible in the Django admin panel.
admin.site.register(Profile)



# Registering the FoodItem model with additional configurations.
@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price') 
    search_fields = ('name', 'category') 
    list_filter = ('category',)  

admin.site.register(Order)
