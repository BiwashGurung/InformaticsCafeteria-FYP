from django import forms
from .models import EventPopup , FoodItem
# from .models import FoodItem

# handling EventPopup model data
class EventPopupForm(forms.ModelForm):
    class Meta:
        #Specifies the model for tthe form
        model = EventPopup
        fields = ['event_title', 'image', 'start_date', 'end_date']

#handeling FoodItem model daa
class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        # Specifies the fields to include in the form
        fields = ['name', 'category', 'description', 'price', 'image', 'is_in_stock']        
