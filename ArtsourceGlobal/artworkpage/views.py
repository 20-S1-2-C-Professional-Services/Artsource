from django.shortcuts import render, redirect, reverse

from booking.forms import BookArtForm
# from homepage.models import Artwork, Booking
from booking.models import Reservation
from artworkpage.models import Artwork, TagsNames, Category
import datetime
from django.db.models import Q
from user.models import User
from .sendRecommendation import send_notify_email
from django.contrib import auth
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

tags = []


# Create your views here.
def index(request):
    global tags
    if not len(tags):
        tags = TagsNames.objects.values_list("tag_names", flat=True)
    return render(request, 'homepage/index.html', {'tags': tags})


# TODO: add the tag search functions here
def search(request):
    images = []
    art_list = []
    name_list = []
    global tags
    if not len(tags):
        tags = TagsNames.objects.values_list("tag_names", flat=True)
    current_username = request.session.get('user_name')
    if request.method == 'POST':
        # the code to get and store the tags
        tags_input = request.POST.get('tags')  # this is the input string

        if len(tags_input) == 0:
            message = 'please enter the tags or words you want!'
            return render(request, 'user/index.html', {'message': message, 'tags': tags})
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
            return render(request, 'user/index.html', {'message': message, 'tags': tags})

        for i in search_result:
            # if i.artwork_user != current_username and not i.booked:  # ensure the owner will not searched their own artworks
            if i.booked or i.user == current_username:
                continue
            art_list.append(i)
            images.append([i.name, i.image.url])

        for i in art_list:
            name = ""
            names = i.artists.all()
            for n in names:
                name += n.artist_names + " "
            name_list.append(name)

        # store the searched results into this list, only store the url
    return render(request, 'artworks/search.html', {'tt': art_list, 'dd': list(reversed(name_list))})
    # return render(request, "artworks/searchresults.html", {'images': images})


# TODO: add the tag search functions here
def simplesearch(request):
    images = []
    art_list = []
    name_list = []
    current_username = request.session.get('user_name')
    if request.method == 'POST':
        # the code to get and store the tags
        search_input = request.POST.get('searchinput')  # this is the input string

        if len(search_input) == 0:
            message = 'please enter the tags or words you want!'
            return render(request, 'artworks/search.html', {'message': message})
        # at the beginning search was implemented by extra, however, it uses different command for different db
        # Thus us Q instead
        q1 = Q()
        q1.connector = 'OR'
        for i in search_input.split(" "):
            q1.children.append(('tags__icontains', i))  # search the tags column
            q1.children.append(('name__icontains', i))  # search the name
            q1.children.append(('description__icontains', i))  # search the description
            q1.children.append(('artists_string__icontains', i))  # search the artist name string
        search_result = Artwork.objects.filter(q1)
        if len(search_result) == 0:
            message = 'Nothing found, try other tags'
            return render(request, 'artworks/search.html', {'message': message})

        for i in search_result:
            # if i.artwork_user != current_username and not i.booked:  # ensure the owner will not searched their own artworks
            if i.booked or i.user == current_username:
                continue
            art_list.append(i)
            images.append([i.name, i.image.url])

        for i in art_list:
            name = ""
            names = i.artists.all()
            for n in names:
                name += n.artist_names + " "
            name_list.append(name)

        # store the searched results into this list, only store the url
    return render(request, 'artworks/search.html', {'tt': art_list, 'dd': list(reversed(name_list))})
    # return render(request, "artworks/searchresults.html", {'images': images})


def recommend(request):
    if request.method == 'POST':
        max_price = request.POST.get('max_price')
        min_price = request.POST.get('min_price')
        max_length = request.POST.get('max_length')
        min_length = request.POST.get('min_length')
        max_height = request.POST.get('max_height')
        min_height = request.POST.get('min_height')
        max_width = request.POST.get('max_width')
        min_width = request.POST.get('min_width')
        additionalnotes = request.POST.get('additionalnotes')
        current_username = request.session.get('user_name')
        user = User.objects.get(username=current_username)
        email = user.email
        postcode = user.additionalInfo.postalCode
        send_notify_email(email, current_username, postcode, max_price, min_price,
                          max_length, min_length, max_width, min_width, max_height, min_height, additionalnotes)

    message = 'The recommendation request was sent to administrator, please check your email later!'
    return render(request, 'user/index.html', {'message': message})


def view_category(request):
    categories = Category.objects.all()

    return render(request, 'artworks/view_category.html', locals())


def create_category(request):
    if request.method == 'POST':
        user_id = request.session.get('_auth_user_id')
        if user_id is not None:
            admin = auth.models.User.objects.get(id=user_id)
            if admin.is_superuser:
                title = request.POST.get('title')
                image_bytes = request.FILES.get('banner').read()
                image_io = io.BytesIO()
                image_io.write(image_bytes)
                image_file = InMemoryUploadedFile(image_io, None, '{}.jpg'.format(title), 'image/jpeg',
                                                  image_io.getbuffer().nbytes, None)
                category = Category()
                category.title = title
                category.tags_list = request.POST.get('tags_list')
                artwork_list = request.POST.get('artwork_list')
                category.artwork_name_list = artwork_list
                category.banner = image_file
                category.save()
                for i in artwork_list.split(" "):
                    chose_artwork = Artwork.objects.get(name=i)  # the needed object
                    category.artwork_list.add(chose_artwork)
                return redirect('/artworkpage/view_category/')
            else:
                message = "you dont have permission to create category! please login in as superuser"
                return render(request, 'artworks/create_category.html', locals())
        message = "please log in as super user!"
        return render(request, 'artworks/create_category.html', locals())

    else:
        all_images = Artwork.objects.all()
        images = []
        name_list = []
        tags_list = TagsNames.objects.values_list('tag_names', flat=True)
        for i in all_images:
            images.append([i.name, i.thumbnail.url])
            name_list.append(i.name)
        return render(request, 'artworks/create_category.html', locals())


def change_category(request):
    user_id = request.session.get('_auth_user_id')
    if user_id is not None:
        admin = auth.models.User.objects.get(id=user_id)
        if admin.is_superuser:
            title = request.POST.get('title')
            category = Category.objects.get(title=title)
            if request.FILES.get('banner') is not None:
                image_bytes = request.FILES.get('banner').read()
                image_io = io.BytesIO()
                image_io.write(image_bytes)
                image_file = InMemoryUploadedFile(image_io, None, '{}.jpg'.format(title), 'image/jpeg',
                                                  image_io.getbuffer().nbytes, None)
                category.banner = image_file
            category.tags_list = request.POST.get('tags_list')
            artwork_list = request.POST.get('artwork_list')
            category.artwork_name_list = artwork_list
            category.save()
            category.artwork_list.clear()  # this is much faster than compare one by one
            for i in artwork_list.split(" "):
                chose_artwork = Artwork.objects.get(name=i)  # the needed object
                category.artwork_list.add(chose_artwork)
            return redirect('/artworkpage/view_category/')
    return redirect('/artworkpage/view_category/')


def edit_category(request):
    title = request.POST.get('category_title')
    category = Category.objects.get(title=title)
    name_list = []
    tags_list = TagsNames.objects.values_list('tag_names', flat=True)
    name_list = Artwork.objects.values_list('name', flat=True)

    return render(request, 'artworks/edit_category.html', locals())


def delete_category(request):
    title = request.POST.get('category_title')
    category = Category.objects.get(title=title)
    category.artwork_list.clear()
    category.delete()
    return


# TODO:the below code is useless, I just put it here, remember delete later
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
