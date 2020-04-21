import random

from django.shortcuts import render
from django.http import HttpResponse
# from homepage.models import Artwork
from artworkpage.models import Artwork

def index(request):
    count = Artwork.objects.count()
    if count > 10:
        sample = random.sample(range(count), 10)
        artwork = [Artwork.objects.all()[i] for i in sample]
    else:
        artwork = Artwork.objects.all()

    last = Artwork.objects.all().reverse()[0:1]
    return render(request, 'gallery/index.html', {'artwork': artwork, 'last': last})


# def artwork_detail(request, pk):
#     artid = Artwork.objects.get(id=pk)
#     return render(request, './artworkpage/index.html', {'artid': artid})
