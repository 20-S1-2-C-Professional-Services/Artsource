import random

from django.shortcuts import render
from django.http import HttpResponse
# from homepage.models import Artwork
from artworkpage.models import Artwork
from artworkpage.models import Category
from itertools import chain


def index(request):
    all_artworks = Artwork.objects.filter(booked=False)
    display_artwork = all_artworks[1:3]
    artwork = all_artworks[4:]
    return render(request, 'gallery/index.html', {'artwork': artwork, 'display_artwork': display_artwork, 'categories': Category.objects.all()})
