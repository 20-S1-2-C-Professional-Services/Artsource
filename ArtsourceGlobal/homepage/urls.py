from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
   path('index/', views.index, name='test'),
   path('index/<int:pk>/', views.artwork_detail, name='artwork_detail'),
   # path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
   path('booking/<int:pk>/', views.booking_detail),
   path('search/', views.search),
]
