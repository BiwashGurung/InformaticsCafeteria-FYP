from django.contrib import admin
from .models import Profile, FoodItem 


admin.site.register(Profile)



@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price') 
    search_fields = ('name', 'category') 
    list_filter = ('category',)  