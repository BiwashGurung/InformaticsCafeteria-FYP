from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class ProfileForm(forms.ModelForm):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password', 'class': 'form-control'}),
        required=False,
        min_length=8,
        help_text='Minimum 8 characters.'
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
        # Set email from User
        self.fields['email'].initial = self.instance.email if self.instance.email else 'No email set'
        # Add phone from Profile
        try:
            profile = self.instance.profile
            phone_initial = profile.phone if profile.phone else 'Not provided'
        except Profile.DoesNotExist:
            phone_initial = 'Not provided'
        self.fields['phone'] = forms.CharField(
            label='Phone Number',
            initial=phone_initial,
            widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            required=False
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise ValidationError('Passwords do not match.')
            if len(new_password) < 8:
                raise ValidationError('Password must be at least 8 characters long.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')

        if new_password:
            user.set_password(new_password)
        
        if commit:
            user.save()
            # Ensure Profile exists and sync username
            profile, created = Profile.objects.get_or_create(user=user)
            profile.username = user.username
            profile.save()
        
        return user