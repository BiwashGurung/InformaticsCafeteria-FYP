from django import forms
from .models import EventPopup , FoodItem
# from .models import FoodItem

# handling EventPopup model data
class EventPopupForm(forms.ModelForm):
    class Meta:
        model = EventPopup
        fields = ['event_title', 'image', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

#handeling FoodItem model data
class FoodItemForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('', 'Select a category'),  
        ('BreakFast', 'BreakFast'),
        ('Appetizer', 'Appetizer'),
        ('Beverages', 'Beverages'),
        ('Desserts', 'Desserts'),
        ('Main Course', 'Main Course'),
        ('Snacks', 'Snacks'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'description', 'price', 'image', 'is_in_stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_in_stock': forms.CheckboxInput(),
        }

       
