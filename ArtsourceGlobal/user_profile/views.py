from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import EditProfileForm, UploadArtForm
from django.contrib import messages
from homepage.models import Artwork, Booking
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from user.models import User
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
from homepage.models import Artwork, Booking


def index(request):
    return render(request, 'user_profile/uprofile.html')


@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'user_profile/userDash.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('view_profile')
        else:
            return redirect('/change_password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'change-password.html', args)


def upload_artwork(request):
    if request.method == 'GET':
        form = UploadArtForm()
        return render(request, 'user_profile/upload_artwork.html', {'form': form})

    else:
        form = UploadArtForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            title = form.cleaned_data['title']
            art_description = form.cleaned_data['art_description']
            height = form.cleaned_data['height']
            width = form.cleaned_data['width']
            price_per_day = form.cleaned_data['price_artwork_per_day']
            artwork_image = UploadArtForm(request.FILES['artwork_image'])
            return redirect('view_profile')
            # args = {'form':form, 'title':title, 'art_description':art_description, 'height':height, 'width':width,'price_per_day':price_per_day,'artwork_image':artwork_image}
        return render(request, 'user_profile/upload_artwork.html', {'form': form})
