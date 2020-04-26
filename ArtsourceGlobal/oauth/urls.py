from django.conf.urls import url
from django.urls import path, include
from oauth import views


urlpatterns = [
    path('instagram/', views.instagram),
    path('instagram_callback/', views.instagram_callback),
    path('facebook/', views.facebook),
    path('facebook_callback/', views.facebook_callback),
    # path('github/', views.github),
    # path('github_callback/', views.github_callback),
    # url(r'^active/(?P<active_code>.*)/$', views.ActiveUserView.as_view(), name="user_active"),
    # url(r'^reset/(?P<reset_code>.*)/$', views.UserResetView.as_view(), name="user_reset"),
    # (?P<active_code# >.*)/$ extract the string and assign to active_code
]