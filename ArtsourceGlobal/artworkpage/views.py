from django.shortcuts import render
from homepage.models import Artwork,Booking
from booking.models import Reservation
# Create your views here.
def index(request):
    artworks = Artwork.objects.all()
    return render(request, 'artworkpage/index.html', {{'artworks':artworks}})
    
def booking_detail(request, pk):
   artid = Artwork.objects.get(id=pk)
   return render(request,'./booking/bookart.html', {'artid': artid})    

def bookArt(request, pk):
    artid = Artwork.objects.get(id=pk)
    if request.method == 'GET':
        form = BookArtForm()
        args = {'artid': artid, 'form':form,}
        return render(request, 'booking/bookart.html',args)
    else:
        form= BookArtForm(request.POST)
        if form.is_valid():
            checkin = form.cleaned_data['CheckIn']
            checkout = form.cleaned_data['CheckOut']
            delta = calc_delta(checkin,checkout)
            total_price_booking = calc_price(artid.price_artwork_per_day, delta.days)
            string_date = convert_to_str(delta)
            return render(request, './booking/bookart.html', {'checkin':checkin,'checkout':checkout, 'artid':artid, 'delta':delta, 'total_price_booking':total_price_booking,'string_date':string_date})

def ReviewBooking(request,checkin,checkout, artid, delta, total_price):
      return render(request, 'finaliseBooking', {'checkin':checkin,'checkout':checkout, 'artid':artid, 'delta':delta, 'total_price_booking':total_price_booking,'string_date':string_date})


#'checkin':checkin,'checkout':checkout

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
    return render(request, 'booking/review.html',{'form':form})




def calc_delta (checkin, checkout):
    date_format = "%Y-%m-%d"
    date1= datetime.strptime(str(checkin), date_format)
    date2=datetime.strptime(str(checkout), date_format)
    delta = date2 - date1
    return delta


def calc_price(price, delta):
    total_price = price*delta
    return total_price


def convert_to_str(delta):
    return str(delta)





