import random

from django.shortcuts import render
from django.http import HttpResponse
# from homepage.models import Artwork
from artworkpage.models import Artwork
from gallery.models import Category


def index(request):
    all_artworks = Artwork.objects.filter(booked=False)
    reset_categories()
    categories = Category.objects.all()
    display_artwork = all_artworks[1:3]
    artwork = all_artworks[4:]
    return render(request, 'gallery/index.html', {'artwork': artwork, 'display_artwork': display_artwork, 'categories': select_categories()})


def select_categories():
    all_categories = Category.objects.all()
    return all_categories


# For testing purposes
def reset_categories():
    Category.objects.all().delete()
    for i in range(1, 3):
        instance = Category.objects.create(name=i)
        instance.banner_artwork=Artwork.objects.filter(booked=False)[0].thumbnail
