from .models import Reservation
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class BookArtForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('CheckIn', 'CheckOut')
        exclude = None
        widgets = {
            'CheckIn': forms.DateTimeInput(attrs={'class': 'datetime-input', 'type': 'date'}),
            'CheckOut': forms.DateTimeInput(attrs={'class': 'datetime-input', 'type': 'date'}),
        }
