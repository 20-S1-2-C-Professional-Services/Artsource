from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.contrib import messages
from django.http import HttpResponse
from artworkpage.models import Artwork
from artworkpage.models import TagsNames


# Create your views here.
def index(request):
    artworks = Artwork.objects.all()
    tags = TagsNames.objects.values_list("tag_names")
    return render(request, 'homepage/index.html', {'artworks': artworks, 'tags': tags})


def successView(request):
    return render(request, 'success.html')


def artwork_detail(request, pk):
    artid = Artwork.objects.get(id=pk)
    return render(request, './artworkpage/index.html', {'artid': artid})


def booking_detail(request, pk):
    artid = Artwork.objects.get(id=pk)
    return render(request, './booking/bookart.html', {'artid': artid})
