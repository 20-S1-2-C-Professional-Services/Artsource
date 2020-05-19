import io
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from django.views import View

from user import models
from .email_send import send_code_email
from .form import UserForm, RegisterForm, ProfileForm, ResetForm, RetrieveForm, UploadForm
import hashlib
from PIL import Image
from artworkpage.models import TagsNames, ArtistNames, Artwork
from .models import EmailVerifyRecord
from booking.models import Reservation
from artworkpage.Image_tools import crop
import base64
import os
from django.contrib import auth
from django.contrib.auth.models import User as AdminUser

# TODO: this tag list should be empty, I set values for test
tags = ['dog', 'peppers', 'mandm', 'mountain', 'civilization']
artists_list = []


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                # search user by email
                active_user = models.User.objects.get(email=email)
                request.session['user_name'] = active_user.username
                # activate user
                active_user.is_active = True
                active_user.save()
                record.delete()  # the record not longer needed
                request.session['is_login'] = True
                request.session['user_id'] = active_user.id
                return redirect('/user/index/')

        else:
            # probably need resend
            return render(request, "verification_fail.html")


class UserResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                # search user by email
                active_user = models.User.objects.get(email=email)
                request.session['user_name'] = active_user.username
                # activate user
                record.delete()  # the record not longer needed
                return redirect('/user/reset/')
        else:
            # probably need resend
            return render(request, "verification_fail.html")


# Use fore reset the password
def reset(request):
    if request.method == 'POST':
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            user_name = request.session['user_name']
            user = models.User.objects.get(username=user_name)
            password1 = reset_form.cleaned_data['new_password1']
            password2 = reset_form.cleaned_data['new_password2']
            if password1 != password2:
                message = 'Passwords are not the same'
                return render(request, "user/reset_password.html", {'message': message})
            user.password = password1
            message = 'Password reset successfully, please login'
            return render('/user/login', {'message': message})
        message = 'The form is invalid, please check your form'
        return render(request, "user/reset_password.html", {'message': message})
    message = 'please enter your new password'
    reset_form = ResetForm()
    return render(request, "user/reset_password.html", {'message': message, 'reset_form': reset_form})


# respond to the "forget password link"
def retrieve(request):
    if request.method == 'POST':
        retrieve_form = RetrieveForm(request.POST)
        if retrieve_form.is_valid():
            email = retrieve_form.cleaned_data['email']
            if models.User.objects.filter(email=email):
                success = send_code_email(email, send_type="reset")
                if success:
                    return render(request, "user/success_send.html")
                else:
                    message = 'failed to send email that cannot reset password now'
                    return render(request, 'user/retrieve_password.html', locals())
            else:
                message = 'The email does not exist'
                return render(request, "user/retrieve_password.html", {'message': message})
        message = 'The form is invalid, please check your form'
        return render(request, "user/retrieve_password.html", {'message': message})
    retrieve_form = RetrieveForm()
    return render(request, "user/retrieve_password.html", {'retrieve_form': retrieve_form})


def login(request):
    if request.session.get('is_login', None):  # reject login if already logged in
        return redirect('/user/index')

    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = 'Please check the provided information'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(username=username)
                if not user.is_active:
                    message = 'Please verify email first'
                    return render(request, 'user/login.html', locals())
                # match the hashcode
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect('/user/index/')
                else:
                    message = 'password is incorrect'
            except Exception as e:
                print(e)
                message = 'username is not exist'
        return render(request, 'user/login.html', locals())
    login_form = UserForm()
    # return render(request, 'user/login.html')
    return render(request, 'user/login.html', locals())


def index(request):
    user_id = request.session.get('_auth_user_id')
    if user_id is not None:
        request.session['is_login'] = True
        request.session['user_id'] = user_id
        request.session['user_name'] = 'Administrator'
    global tags
    if not len(tags):
        tags = TagsNames.objects.values_list("tag_names", flat=True)
    return render(request, 'user/index.html', {'tags': tags})


def register(request):
    if request.session.get('is_login', None):
        # cant register when logged in
        return redirect('/user/index/')

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        # Get the form
        # check_box_list = request.POST.getlist('check_box_list')
        # for i in check_box_list:
        #     print(check_box_list)
        #     if i == '1':
        #         print("the form returns integer")
        #     print("the term function")  # i.e. add the term choice to db
        message = ''
        check_term = request.POST.get('term_check')  # another method to get check box, or can use form.cleaned_data

        if check_term == 'on':
            stored_form = register_form
            if register_form.is_valid():
                # dont wanna fill form again
                # username = register_form.cleaned_data['username']
                register_form.clean()
                username = request.POST.get('username')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                email = request.POST.get('email')

                # check passwords are the same
                if password1 != password2:
                    message = 'Not the same password'
                    return render(request, 'user/register.html', {'message': message, 'register_form': stored_form})
                else:
                    same_name_user = models.User.objects.filter(username=username)
                    # check user name
                    if same_name_user:
                        message = 'The user name was already existed'
                        return render(request, 'user/register.html',
                                      {'message': message, 'register_form': stored_form})

                    same_email_user = models.User.objects.filter(email=email)
                    if same_email_user:
                        message = 'The email was registered, please use another one'
                        return render(request, 'user/register.html',
                                      {'message': message, 'register_form': stored_form})

                    artist = request.POST.get('artist')
                    if artist == 'on':
                        ref_email = request.POST.get('refEmail')
                        if models.User.objects.filter(email=ref_email):
                            message = 'Sorry, cant find your referee\'s email'
                            return render(request, 'user/register.html',
                                          {'message': message, 'register_form': stored_form})

                    # create the user
                    new_user = models.User()
                    new_user.instagram_username = request.POST.get('instagram_username')
                    new_user.username = username
                    # use encrypted password
                    new_user.password = hash_code(password1)
                    new_user.email = email
                    new_user.is_active = False
                    # record additional info
                    additional_info = request.POST.get('additionalInfo')
                    street1 = request.POST.get('street1')
                    additionalInfo = models.AdditionalInfo()
                    additionalInfo.gender = request.POST.get('gender')
                    if additional_info == 'on' or street1 != '':  # they may fill the form and close the tab
                        additionalInfo.age = int(request.POST.get('age'))
                        additionalInfo.street1 = street1
                        additionalInfo.street2 = request.POST.get('street2')
                        additionalInfo.suburb = request.POST.get('suburb')
                        additionalInfo.state = request.POST.get('state')
                        additionalInfo.postalCode = request.POST.get('postalCode')
                        additionalInfo.country = request.POST.get('country')
                        additionalInfo.phone = request.POST.get('phone')

                    # record interest
                    interest = models.Interest()
                    if request.POST.get('painting') == 'on':
                        interest.painting = True
                    if request.POST.get('sculpture') == 'on':
                        interest.sculpture = True
                    if request.POST.get('photography') == 'on':
                        interest.photography = True
                    if request.POST.get('calligraphy') == 'on':
                        interest.calligraphy = True
                    if request.POST.get('printmaking') == 'on':
                        interest.printmaking = True
                    if request.POST.get('artsAndCrafts') == 'on':
                        interest.artsAndCrafts = True
                    if request.POST.get('sealCutting') == 'on':
                        interest.sealCutting = True
                    if request.POST.get('artDesign') == 'on':
                        interest.artDesign = True

                    if artist == 'on':
                        new_user.artist = True
                        ref_email = request.POST.get('refEmail')
                        new_user.refEmail = ref_email
                        real_name = request.POST.get('realName')
                        success = send_code_email(email, referee_email=ref_email, send_type="register",
                                                  real_name=real_name, is_artist=True)
                    else:
                        success = send_code_email(email, send_type="register")
                    if success:
                        try:
                            additionalInfo.save()
                            interest.save()
                            new_user.interest = interest
                            new_user.additionalInfo = additionalInfo
                            new_user.save()
                        except Exception as e:
                            print(e)
                        return render(request, "user/success_send.html")
                    else:
                        message = 'failed to send email that cannot register you now'
                        return render(request, 'user/register.html', {'message': message, 'register_form': stored_form})
            message = 'Please check the provided information such as Captcha'
            return render(request, 'user/register.html', {'message': message, 'register_form': stored_form})
    # if request is not valid, return a RegisterForm
    register_form = RegisterForm()
    message = ''
    # render a form with error message
    return render(request, 'user/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # no login, no logout
        return redirect('/user/index/')
    request.session.flush()
    # or we can use the code below, should has the same effect if dont add new session keys
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/user/index/')


# The hash function used to encrypt password
def hash_code(s, salt='artsource'):
    h = hashlib.sha256()
    s += salt
    # update only accept bytes
    h.update(s.encode())
    return h.hexdigest()


def profile(request):
    # TODO: currently I put the interface to show admin tool here, maybe change later
    user_id = request.session.get('_auth_user_id')
    if user_id is not None:
        admin = auth.models.User.objects.get(id=user_id)
        if admin.is_superuser:
            images = []
            booked_records = Reservation.objects.all()
            for record in booked_records:
                if record.artwork_booked is not None:
                    if record.artwork_booked.booked:
                        images.append([record.artwork_booked.name, record.artwork_booked.image.url, True])
                    else:
                        images.append([record.artwork_booked.name, record.artwork_booked.image.url])

            return render(request, 'user/profile.html', {"lent": True, "images": images, "admin": True})

    # The normal user's profile
    current_user_name = request.session.get('user_name')
    user = models.User.objects.get(username=current_user_name)
    images = []
    if user.artwork_user is not None:
        artworks = user.artwork_user.values_list("name", "image")
        for artwork in artworks:
            name = artwork[0]
            url = '/media/' + artwork[1]
            images.append([name, url])
    return render(request, 'user/profile.html', {"profile": True, "images": images})


def edit_profile(request):
    # check select_related latter
    current_user_name = request.session.get('user_name')
    user = models.User.objects.get(username=current_user_name)
    additionalInfo = user.additionalInfo
    interest = user.interest
    message = ''
    if request.method == 'POST':
        # record user's modification
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            new_user_name = profile_form.cleaned_data['username']
            if new_user_name != user.username:
                same_user_name = models.User.objects.filter(username=new_user_name)
                if same_user_name:
                    message = 'The user name was already existed'
                    profile_form.username = user.username
                    return render(request, 'user/editProfile.html', {'message': message, 'profile_form': profile_form})
                user.username = new_user_name
                user.save()
                request.session['user_name'] = user.username
            additionalInfo.gender = profile_form.cleaned_data['gender']
            additionalInfo.age = profile_form.cleaned_data['age']
            additionalInfo.street1 = profile_form.cleaned_data['street1']
            additionalInfo.street2 = profile_form.cleaned_data['street2']
            additionalInfo.state = profile_form.cleaned_data['state']
            additionalInfo.suburb = profile_form.cleaned_data['suburb']
            additionalInfo.postalCode = profile_form.cleaned_data['postalCode']
            additionalInfo.country = profile_form.cleaned_data['country']
            additionalInfo.phone = profile_form.cleaned_data['phone']
            additionalInfo.save()
            interest.painting = profile_form.cleaned_data['painting']
            interest.sculpture = profile_form.cleaned_data['sculpture']
            interest.photography = profile_form.cleaned_data['photography']
            interest.calligraphy = profile_form.cleaned_data['calligraphy']
            interest.printmaking = profile_form.cleaned_data['printmaking']
            interest.artsAndCrafts = profile_form.cleaned_data['art_and_craft']
            interest.sealCutting = profile_form.cleaned_data['seal_cutting']
            interest.artDesign = profile_form.cleaned_data['art_design']
            interest.save()

            return redirect('/user/profile/')
        message = 'The form is invalid'

    profile_form = ProfileForm(initial={
        'username': user.username,
        'age': additionalInfo.age,
        'gender': additionalInfo.gender,
        'street1': additionalInfo.street1,
        'street2': additionalInfo.street2,
        'state': additionalInfo.state,
        'suburb': additionalInfo.suburb,
        'postalCode': additionalInfo.postalCode,
        'country': additionalInfo.country,
        'phone': additionalInfo.phone,
        'painting': interest.painting,
        'sculpture': interest.sculpture,
        'photography': interest.photography,
        'calligraphy': interest.calligraphy,
        'printmaking': interest.printmaking,
        'art_and_craft': interest.artsAndCrafts,
        'seal_cutting': interest.sealCutting,
        'art_design': interest.artDesign,
    })

    return render(request, 'user/editProfile.html', {'message': message, 'profile_form': profile_form})


def register_middle(request):
    return render(request, "user/register_middle.html")


def upload_artwork(request):
    global tags
    if not len(tags):
        tags = TagsNames.objects.values_list("tag_names", flat=True)
        if not len(tags):
            tags = []

    global artists_list
    if not len(artists_list):
        current_artists_list = ArtistNames.objects.values_list("id", "artist_names")
        for i in current_artists_list:
            artists_list.append((i[0], i[1]))

    if request.method == 'POST':
        upload_type = request.POST.get('upload_type')
        name = request.POST.get('name')
        if upload_type == 'upload':
            if Artwork.objects.filter(name=name):
                message = "This name already exist!"
                return render(request, "user/upload_artwork.html", {'message': message, 'tags': tags})
            else:
                artwork = Artwork()
        else:
            try:
                artwork = Artwork.objects.get(name=name)
            except Exception as e:
                print(e)
                message = "Can find this artwork!"
                return render(request, "user/upload_artwork.html", {'message': message, 'tags': tags})
        current_user_name = request.session.get('user_name')
        user = models.User.objects.get(username=current_user_name)
        artwork.name = name
        artwork.description = request.POST.get('description')
        artwork.length = 0 #request.POST.get('length') ## This is not a necessary value for MVP I think, temporarily removed - JT
        artwork.width = request.POST.get('width')
        artwork.height = request.POST.get('height')
        if request.FILES.get('image') is not None:
            image_bytes = request.FILES.get('image').read()
            image_io = io.BytesIO()
            image_io.write(image_bytes)
            image_file = InMemoryUploadedFile(image_io, None, '{}.jpg'.format(name), 'image/jpeg',
                                              image_io.getbuffer().nbytes, None)

            artwork.image = image_file

        thumbnail = request.POST.get('thumbnail')
        code = thumbnail.replace('data:image/jpeg;base64,', '')
        thumb_data = base64.b64decode(code)
        thumb_io = io.BytesIO()
        thumb_io.write(thumb_data)
        thumb_file = InMemoryUploadedFile(thumb_io, None, '{}.jpg'.format(name + "_thumbnail"), 'image/jpeg',
                                          thumb_io.getbuffer().nbytes, None)
        artwork.thumbnail = thumb_file
        artwork.user = user
        # save the price
        artwork.price = request.POST.get('price')
        # the code to get and store the tags

        tags_input = request.POST.get('tags')
        # Make the input more robust
        artwork.tags = tags_input

        # so this should be the line to store tags
        # update the tags
        if len(tags_input.replace(" ", "")) > 0:
            for i in tags_input.split(" "):
                if i not in tags:
                    print(i)
                    print(tags)
                    tags.append(i)
                    new_tag = TagsNames()
                    new_tag.tag_names = i
                    new_tag.save()
        artists_input = request.POST.get('artists')
        artwork.artists_string = artists_input
        artwork.save()
        for i in artists_input.split(" "):
            artist_info = i.split(",")
            if len(artist_info) > 1:
                exist_artist = ArtistNames.objects.filter(id=artist_info[1])
                if exist_artist:
                    if not artwork.artists.filter(id=artist_info[1]):
                        artwork.artists.add(ArtistNames.objects.get(id=artist_info[1]))
            else:
                new_artist = ArtistNames()
                new_artist.artist_names = artist_info[0]
                new_artist.save()
                artwork.artists.add(new_artist)
                artists_list.append((artist_info[0], new_artist.id))

        return redirect('/user/profile/')

    return render(request, "user/upload_artwork.html", {'tags': tags, 'artists': artists_list})


def edit_artwork(request):
    global tags
    if not len(tags):
        tags = TagsNames.objects.values_list("tag_names", flat=True)
        if not len(tags):
            tags = []

    global artists_list
    if not len(artists_list):
        artists_list = ArtistNames.objects.values_list("id", "artist_names")
        if not len(artists_list):
            artists_list = []
    if request.method == 'POST':
        name = request.POST.get('name')
        artwork = Artwork.objects.filter(name=name).first()
        if artwork:
            name = artwork.name
            image = artwork.image.url
            tag_string = artwork.tags
            price = artwork.price
            thumbnail = artwork.thumbnail
            artwork_id = artwork.id
            related_artists = artwork.artists.all()
            artists_string = ""
            for i in related_artists:
                artists_string = artists_string + " " + i.artist_names + "," + i.id

    return render(request, "user/edit_artwork.html", locals())


def delete_artwork(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        artwork = Artwork.objects.filter(name=name).first()
        if artwork:
            img_addr = os.path.join(os.path.abspath('.'), "media/" + str(artwork.image))
            thumb_addr = os.path.join(os.path.abspath('.'), "media/" + str(artwork.thumbnail))
            os.remove(img_addr)
            os.remove(thumb_addr)
            artwork.delete()  # delete the record in db
    return redirect('/user/profile/')


def booked_artwork(request):
    user_name = request.session.get('user_name')
    user = models.User.objects.get(username=user_name)
    images = []
    if user.renter is not None:
        booked_records = user.renter.all()
        for record in booked_records:
            if record.artwork_booked is not None:
                images.append([record.artwork_booked.name, record.artwork_booked.image.url])
    return render(request, 'user/profile.html', {"booked": True, "images": images})


def lent_artwork(request):
    user_name = request.session.get('user_name')
    user = models.User.objects.get(username=user_name)
    images = []
    if user.owner is not None:
        booked_records = user.owner.all()
        for record in booked_records:
            if record.artwork_booked is not None:
                if record.artwork_booked.booked:
                    images.append([record.artwork_booked.name, record.artwork_booked.image.url, True])
                else:
                    images.append([record.artwork_booked.name, record.artwork_booked.image.url])
    return render(request, 'user/profile.html', {"lent": True, "images": images})
