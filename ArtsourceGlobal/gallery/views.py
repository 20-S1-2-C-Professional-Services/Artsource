import random

from django.shortcuts import render
from django.http import HttpResponse
# from homepage.models import Artwork
from artworkpage.models import Artwork

def index(request):
    display_artwork = Artwork.objects.all()[1:3]
    artwork = Artwork.objects.all()[4:]
    return render(request, 'gallery/index.html', {'artwork': artwork, 'display_artwork': display_artwork})


# def artwork_detail(request, pk):
#     artid = Artwork.objects.get(id=pk)
#     return render(request, './artworkpage/index.html', {'artid': artid})
