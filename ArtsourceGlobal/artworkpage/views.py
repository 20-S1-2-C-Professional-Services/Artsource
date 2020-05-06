from django.shortcuts import render, redirect, reverse

from booking.forms import BookArtForm
from homepage.models import Artwork, Booking
from booking.models import Reservation
from artworkpage.models import Artwork
import datetime
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request, 'artworkpage/index.html')


# TODO: add the tag search functions here
def search(request):
    images = []
    current_username = request.session.get('user_name')
    if request.method == 'POST':
        # the code to get and store the tags
        tags_input = request.POST.get('tags')  # this is the input string

        if len(tags_input) == 0:
            message = 'please enter the tags or words you want!'
            return render(request, 'homepage/index.html', {'message': message})
        # at the beginning search was implemented by extra, however, it uses different command for different db
        # Thus us Q instead
        q1 = Q()
        q1.connector = 'OR'
        for i in tags_input.split(" "):
            q1.children.append(('tags__icontains', i))  # search the tags column
            q1.children.append(('name__icontains', i))  # search the name
        search_result = Artwork.objects.filter(q1)

        if len(search_result) == 0:
            message = 'Nothing found, try other tags'
            return render(request, 'homepage/index.html', {'message': message})
        for i in search_result:
            if i.artwork_user.username != current_username:  # ensure the owner will not searched their own artworks
                images.append([i.name, i.image.url])

        # store the searched results into this list, only store the url
    return render(request, "artworks/searchresults.html", {'images': images})


def booking_detail(request, pk):
    artid = Artwork.objects.get(id=pk)
    return render(request, './booking/bookart.html', {'artid': artid})


def bookArt(request, pk):
    artid = Artwork.objects.get(id=pk)
    if request.method == 'GET':
        form = BookArtForm()
        args = {'artid': artid, 'form': form, }
        return render(request, 'booking/bookart.html', args)
    else:
        form = BookArtForm(request.POST)
        if form.is_valid():
            checkin = form.cleaned_data['CheckIn']
            checkout = form.cleaned_data['CheckOut']
            delta = calc_delta(checkin, checkout)
            total_price_booking = calc_price(artid.price_artwork_per_day, delta.days)
            string_date = convert_to_str(delta)
            return render(request, './booking/bookart.html',
                          {'checkin': checkin, 'checkout': checkout, 'artid': artid, 'delta': delta,
                           'total_price_booking': total_price_booking, 'string_date': string_date})


def ReviewBooking(request, checkin, checkout, artid, delta, total_price, total_price_booking, string_date):
    return render(request, 'finaliseBooking', {'checkin': checkin, 'checkout': checkout, 'artid': artid, 'delta': delta,
                                               'total_price_booking': total_price_booking, 'string_date': string_date})


# 'checkin':checkin,'checkout':checkout

def finaliseBooking(request, artid, checkin, checkout, totalcost):
    if request.method == 'POST':
        form = BookArtForm(request.POST)
        book = form.save(commit=False)
        book.user = request.user
        book.save()
        art = form.cleaned_data['artid']
        CheckIn = form.cleaned_data['checkin']
        CheckOut = form.cleaned_data['checkout']
        totalPrice = form.cleaned_data['totalcost']
        link = reverse('bookArt')
        return redirect(link)
        form = BookArtForm()
    return render(request, 'booking/review.html', {'form': form})


def calc_delta(checkin, checkout):
    date_format = "%Y-%m-%d"
    date1 = datetime.strptime(str(checkin), date_format)
    date2 = datetime.strptime(str(checkout), date_format)
    delta = date2 - date1
    return delta


def calc_price(price, delta):
    total_price = price * delta
    return total_price


def convert_to_str(delta):
    return str(delta)
