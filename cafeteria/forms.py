from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from .models import Profile
import logging

logger = logging.getLogger(__name__)

class ProfileForm(forms.ModelForm):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password', 'class': 'form-control'}),
        required=False,
        min_length=8,
        help_text='Minimum 8 characters, must be different from current password.'
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # Setting the email from User
        self.fields['email'].initial = self.instance.email if self.instance.email else 'No email set'
        # Defingm the phone field without initial value
        self.fields['phone'] = forms.CharField(
            label='Phone Number',
            widget=forms.TextInput(attrs={'placeholder': 'Enter phone number', 'class': 'form-control'}),
            required=False,
            max_length=15,
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        logger.debug(f"Cleaning phone: {phone}")
        if phone:  
            # Checking the uniqueness, excluding current user's profile
            if Profile.objects.exclude(user=self.instance).filter(phone=phone).exists():
                raise ValidationError('This phone number is already in use.')
          
            if not phone.replace('+', '').replace('-', '').isdigit():
                raise ValidationError('Phone number must contain only digits, "+", or "-".')
        return phone

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password and self.instance.check_password(new_password):
            raise ValidationError('New password must be different from your current password.')
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        logger.debug(f"Cleaning form: new_password={bool(new_password)}, phone={cleaned_data.get('phone')}")

        # Only validating the passwords if at least one is provided
        if new_password or confirm_password:
            if new_password != confirm_password:
                raise ValidationError('Passwords do not match.')
            if new_password and len(new_password) < 8:
                raise ValidationError('Password must be at least 8 characters long.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        phone = self.cleaned_data.get('phone')
        logger.debug(f"Saving: username={user.username}, new_password={bool(new_password)}, phone={phone}")

        if new_password:
            user.set_password(new_password)
        
        if commit:
            user.save()
            # Ensuring the Profile exists
            profile, created = Profile.objects.get_or_create(user=user)
            profile.username = user.username
            # Only updating the phone if a new, non-empty value is provided
            if phone:
                profile.phone = phone
            elif created and not profile.phone:
                profile.phone = ''
            profile.save()
            logger.debug(f"Profile saved: phone={profile.phone}")
            # Updating thre session to prevent logout
            if new_password and self.request:
                update_session_auth_hash(self.request, user)
        
        return user