from django.conf.urls import url
from django.urls import path, include
from user import views
from django.contrib import admin


urlpatterns = [
    path('login/', views.login),
    path('index/', views.index),
    path('register_middle/', views.register_middle),
    path('register/', views.register),
    path('logout/', views.logout),
    path('profile/', views.profile),
    path('editProfile/', views.edit_profile),
    path('retrieve/', views.retrieve),
    path('reset/', views.reset),
    path('upload_artwork/', views.upload_artwork),
    path('edit_artwork/', views.edit_artwork),
    path('delete_artwork/', views.delete_artwork),
    path('booked_artwork/', views.booked_artwork),
    path('lent_artwork/', views.lent_artwork),
    url(r'^active/(?P<active_code>.*)/$', views.ActiveUserView.as_view(), name="user_active"),
    url(r'^reset/(?P<reset_code>.*)/$', views.UserResetView.as_view(), name="user_reset"),
    # (?P<active_code# >.*)/$ extract the string and assign to active_code
]