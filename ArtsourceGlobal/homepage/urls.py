from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from django.views.generic.base import TemplateView
from artworkpage import views as artwork_view
from . import views

urlpatterns = [
   path('', views.index),
   path('index/', views.index),
   path('search/', artwork_view.search),
   path('index/<int:pk>/', views.artwork_detail, name='artwork_detail'),
   # path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
   path('booking/<int:pk>/', views.booking_detail),

]
