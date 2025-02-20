from django import forms
from .models import EventPopup , FoodItem
# from .models import FoodItem

class EventPopupForm(forms.ModelForm):
    class Meta:
        model = EventPopup
        fields = ['event_title', 'image', 'start_date', 'end_date']


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'description', 'price', 'image', 'is_in_stock']        
