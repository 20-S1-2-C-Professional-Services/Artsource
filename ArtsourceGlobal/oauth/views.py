import requests
from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
import json
# from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.integrations.requests_client import OAuth2Session
from asg_web_app import settings
from asg_web_app.settings import oauth
from user.models import User, AdditionalInfo, Interest
from user.form import RegisterForm
import requests


# TODO: change the client_id and client_secret
def instagram(request):
    # The below client id and secret should be changed after you get your own id and secret
    redirect_uri = 'https://localhost:8000/oauth/instagram_callback'
    url = "https://api.instagram.com/oauth/authorize?client_id=2861822790566791" \
          "&redirect_uri=" + redirect_uri + "&scope=user_profile&response_type=code"

    return redirect(url)


# TODO: change the client_id and client_secret
def instagram_callback(request):
    code = request.get_full_path().split("code=")[1].split("#_")[0]
    url = "https://api.instagram.com/oauth/access_token/"
    data = {"client_id": "2861822790566791",
            "client_secret": "9f6c11ccc2a1076130eaea5104fc7303",
            "grant_type": "authorization_code",
            "redirect_uri": "https://localhost:8000/oauth/instagram_callback",
            "code": code
            }
    r = requests.post(url, data=data)
    # return redirect(url)
    json_data = json.loads(r.text)
    access_token = json_data.get("access_token")
    user_id = str(json_data.get("user_id"))
    response = requests.get("https://graph.instagram.com/"+user_id+"?fields=id,username&access_token="+access_token)
    username = json.loads(response.text).get("username")
    message = "please create a local account!"
    register_form = RegisterForm(initial={
        'username': username,
    })
    return render(request, "user/register.html", {'message': message, 'register_form': register_form,
                                                  'instagram_username':username})

