from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import bookArt

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search),
    path('simplesearch/', views.simplesearch),
    path('recommend/', views.recommend),
    path('view_category/', views.view_category),
    path('create_category/', views.create_category),
    path('edit_category/', views.edit_category),
    path('delete_category/', views.delete_category),
    path('change_category/', views.change_category),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    re_path('booking/(?P<pk>\d+)', views.bookArt, name='booking'),
    # path('booking/review', views.finaliseBooking, name='review'),
    path('', TemplateView.as_view(template_name='homepage/index.html'), name='home'),
    re_path(
        'booking/review/(?P<artid>[0-9]+)/(?P<checkin>(\d{4}-\d{2}-\d{2}))/(?P<checkout>(\d{4}-\d{2}-\d{2}))/('
        '?P<totalcost>[0-9]+)',
        views.finaliseBooking, name='review'),
]
