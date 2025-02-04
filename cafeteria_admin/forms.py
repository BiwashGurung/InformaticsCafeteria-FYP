from django import forms
from .models import EventPopup

class EventPopupForm(forms.ModelForm):
    class Meta:
        model = EventPopup
        fields = ['event_title', 'image', 'start_date', 'end_date']
