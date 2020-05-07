import random

from django.shortcuts import render
from django.http import HttpResponse
# from homepage.models import Artwork
from artworkpage.models import Artwork


def index(request):
    all_artworks = Artwork.objects.filter(booked=False)
    display_artwork = all_artworks[1:3]
    artwork = all_artworks[4:]
    return render(request, 'gallery/index.html', {'artwork': artwork, 'display_artwork': display_artwork})

# def artwork_detail(request, pk):
#     artid = Artwork.objects.get(id=pk)
#     return render(request, './artworkpage/index.html', {'artid': artid})
