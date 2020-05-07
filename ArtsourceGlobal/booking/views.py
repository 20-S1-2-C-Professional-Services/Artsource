import datetime
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.core.signing import Signer
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from user.models import User
# from Authorize.models import UserRole
# from ManageHotels.models import Photo
from .models import Reservation
from django.shortcuts import render, redirect
from user.models import User
from artworkpage.models import Artwork
from .forms import BookArtForm
from datetime import datetime
from .notifyemail import send_notify_email
import json
from django.views import View
from django.template.loader import get_template


## Generates a PDF using the render help function and outputs it as invoice.html


## Works out how long the user is staying in a hotel for also working out the total cost.
def bookArt(request, pk):
    art_id = int(float(pk))
    artwork = Artwork.objects.get(id=art_id)

    if artwork.booked is None:
        message = "This artwork was booked out already!"
        return render(request, 'user/index.html', locals())

    if request.session.get('user_name') is None:
        message = "Please login first!"
        return render(request, 'user/login.html', locals())

    if artwork.user.username == request.session.get('user_name'):
        message = "This is your artwork, you dont need to book it!"
        return render(request, 'user/index.html', {'message': message})

    if request.method == 'GET':
        form = BookArtForm()
        args = {'artid': artwork, 'form': form}
        return render(request, 'booking/bookart.html', args)
    else:
        form = BookArtForm(request.POST)
        if form.is_valid():
            checkin = form.cleaned_data['CheckIn']
            checkout = form.cleaned_data['CheckOut']
            delta = calc_delta(checkin, checkout)
            total_price_booking = calc_price(artwork.price, delta.days)
            return render(request, 'booking/confirmbooking.html',
                          {'checkin': checkin, 'checkout': checkout, 'name': artwork.name,
                           'single_price': artwork.price, 'duration': delta,
                           'total_price': total_price_booking})


def finish_booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        total_price = request.POST.get('total_price')
        duration = request.POST.get('duration')
        artwork = Artwork.objects.get(name=name)
        reservation = Reservation()
        reservation.artwork_booked = artwork
        reservation.owner = artwork.user
        reservation.renter = User.objects.get(username=request.session.get('user_name'))
        reservation.CheckIn = checkin
        reservation.CheckOut = checkout
        reservation.duration = float(duration.split(' ')[0])
        reservation.totalPrice = total_price
        reservation.save()
        artwork.booked = True
        artwork.save()
        message = 'successfully booked'
        send_notify_email(artwork.user.email, request.session.get('user_name'), name, 'book')
        return render(request, 'booking/review.html', {'message': message, 'checkin': checkin,
                                                       'checkout': checkout, 'name': name,
                                                       'single_price': artwork.price, 'duration': duration,
                                                       'total_price': total_price})

    message = 'No order find'
    return render(request, 'booking/confirmbooking.html',
                  {'message': message})


def review(request):
    if request.method == 'POST':
        message = 'This is the booking details'
        artwork_name = request.POST.get('name')
        artwork = Artwork.objects.get(name=artwork_name)
        if artwork.artwork_booked is not None:
            booking_record = artwork.artwork_booked.first()
            checkin = booking_record.CheckIn
            checkout = booking_record.CheckOut
            name = artwork_name
            duration = booking_record.duration
            total_price = booking_record.totalPrice
            return render(request, 'booking/review.html', {'message': message, 'checkin': checkin,
                                                           'checkout': checkout, 'name': name,
                                                           'single_price': artwork.price, 'duration': duration,
                                                           'total_price': total_price})
    message = 'No order find, redirect to profile'
    return redirect('/user/profile/', {'message': message})


def accept(request):
    if request.method == 'POST':
        message = 'The book confirmed, redirect back'
        artwork_name = request.POST.get('name')
        artwork = Artwork.objects.get(name=artwork_name)
        artwork.booked = True
        if artwork.artwork_booked is not None:
            record = artwork.artwork_booked.first()
            send_notify_email(record.renter.emaill, record.renter.username, artwork_name, 'accept')
            return render(request, 'booking/review.html', {'message': message})
    message = 'No order find'
    return redirect('/user/lent_artwork/', {'message': message})


def cancel(request):
    if request.method == 'POST':
        message = 'The book cancelled, redirect back'
        artwork_name = request.POST.get('name')
        artwork = Artwork.objects.get(name=artwork_name)
        artwork.booked = True
        if artwork.artwork_booked is not None:
            record = Reservation.objects.get(id=artwork.artwork_booked.first().id) # get the reservation record here
            send_notify_email(record.renter.email, record.renter.username, artwork_name, 'cancel')
            send_notify_email(record.owner.email, record.owner.username, artwork_name, 'cancel')
            record.delete()
            artwork.booked = False
            artwork.save()
            return redirect('/user/profile/', {'message': message})
    message = 'No order find'
    return redirect('/user/lent_artwork/', {'message': message})


# seems nothing need to do for this stage, this function also work for finish review
# this function will need split into finish_review and cancel_booking if you want to do
# sth different with these two behaviours
def cancel_booking(request):
    return redirect('/user/index/')


# 'checkin':checkin,'checkout':checkout
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

#
# # Stores the confirmed booking  into the database
# def storeBooking(request, artid, checkin, checkout, totalcost):
#     if request.method == 'POST':
#         user = request.user
#         art = Artwork.objects.get(artid)
#         cost = totalcost
#         newReservation = Reservation()
#         newReservation.booking_owner = user
#         newReservation.art = art
#         newReservation.CheckIn = checkin
#         newReservation.CheckOut = checkout
#         newReservation.totalPrice = cost
#         newReservation.save()
#         # Deletes the session variables.
#         del request.session['checkin']
#         del request.session['checkout']
#         link = reverse('homepage:view_profile')
#         return HttpResponseRedirect(link)
#
#     else:
#         url = reverse('homepage:view_profile')
#         return url
#
#
# def finaliseBooking(request, artid, checkin, checkout, totalcost):
#     if request.method == 'POST':
#         form = BookArtForm(request.POST)
#         book = form.save(commit=False)
#         book.user = request.user
#         book.save()
#         art = form.cleaned_data['artid']
#         CheckIn = form.cleaned_data['checkin']
#         CheckOut = form.cleaned_data['checkout']
#         totalPrice = form.cleaned_data['totalcost']
#         link = reverse('bookArt')
#         return redirect(link)
#         form = BookArtForm()
#     return render(request, 'booking/review.html', {'form': form})
