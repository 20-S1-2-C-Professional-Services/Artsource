from django import forms
from django.contrib.auth.models import User
from homepage.models import Artwork, Booking
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

class UploadArtForm(forms.ModelForm):
    title = forms.CharField(label=("Artwork Title"),required=True),
    art_description = forms.CharField(label=("Description"),required=True),
    height = forms.FloatField(label=("Height of the Artwork"), required=True),
    width = forms.FloatField(label=("Width of the Artwork"), required=True),
    price_per_day = forms.FloatField(label=("Set Price/Day"), required=True),
    artwork_image = forms.FileField(label=("Upload Art"), required=True)
    


    class Meta:
        model = Artwork
        field = ('title','art_description','height','width', 'price_per_day', 'artwork_image',)
        exclude = ('likes', 'date_created', )
