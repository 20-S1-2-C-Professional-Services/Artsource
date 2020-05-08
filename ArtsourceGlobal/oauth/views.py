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


def instagram(request):
    # The below client id and secret should be changed after you get your own id and secret
    redirect_uri = 'https://localhost:8000/oauth/instagram_callback'
    url = "https://api.instagram.com/oauth/authorize?client_id=2861822790566791" \
          "&redirect_uri=" + redirect_uri + "&scope=user_profile&response_type=code"

    return redirect(url)


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


#
# def facebook(request):
#     # The below client id and secret should be changed after you get your own id and secret
#     redirect_uri = 'https://localhost:8000/oauth/facebook_callback'
#     url = "https://www.facebook.com/v6.0/dialog/oauth?client_id=1052296011819502" \
#           "&redirect_uri=" + redirect_uri + "&state={\"st=state123abc,ds=123456789}\""
#
#     return redirect(url)
#
#
# def facebook_callback(request):
#     redirect_uri = 'https://localhost:8000/oauth/facebook_callback'
#     print("in the facebook callback")
#     message = request.get_full_path()
#     print(message)
#     print("this is the body")
#     print(request.body)
#     if message.find("code=") != -1:
#         code = message.split("code=")[1].split("&state=")[0]
#         url = "https://graph.facebook.com/v6.0/oauth/access_token?client_id=1052296011819502&" \
#               "&redirect_uri=" + redirect_uri + "&client_secret=fcb79bc8754e158ea251428f90b96248" + \
#               "&code=" + code
#         return redirect(url)
#
#     # resp = oauth.github.get(url='https://api.github.com/user', token=token)
#     #     profile = resp.json()
#     return render(request, "oauth/index.html", {'message': message})


#
# def github(request):
#     # The below client id and secret should be changed after you get your own id and secret
#     redirect_uri = 'https://localhost:8000/oauth/github_callback'
#     github = oauth.create_client('github')
#     return github.authorize_redirect(request, redirect_uri)
#
#
# def github_callback(request):
#     token = oauth.github.authorize_access_token(request)
#     resp = oauth.github.get(url='https://api.github.com/user', token=token)
#     profile = resp.json()
#     # do something with the token and profile
#     return redirect(request, profile)


def callback_redirect(request, profile):
    message = 'please register your account here!'
    new_user_name = profile['login']
    same_user_name = User.objects.filter(username=new_user_name)
    if same_user_name:
        message += 'The user name was already existed, please choose a new one'
        new_user_name = ''
    email = profile['email']
    if email is None:
        email = ''
    register_form = RegisterForm(initial={
        'username': new_user_name,
        'email': email,
    })
    return render(request, "user/register.html", {'message': message, 'register_form': register_form})


def final_register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
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
                    same_name_user = User.objects.filter(username=username)
                    # check user name
                    if same_name_user:
                        message = 'The user name was already existed'
                        return render(request, 'user/register.html',
                                      {'message': message, 'register_form': stored_form})

                    same_email_user = User.objects.filter(email=email)
                    if same_email_user:
                        message = 'The email was registered, please use another one'
                        return render(request, 'user/register.html',
                                      {'message': message, 'register_form': stored_form})
                interest = Interest()
                user = User()
                additional_info = AdditionalInfo()
                additional_info.save()
                interest.save()
                user.additionalInfo = additional_info
                user.interest = interest
                user.email = email
                user.password = password1
                user.username = username
                user.is_active = True
                user.save()
                # TODO: label as todo to ensure later check
                # the user was logged without verification of their email, may need change here
                request.session['is_login'] = True
                request.session['user_name'] = user.username
                return redirect('/user/index/')

    register_form = RegisterForm()
    message = 'There are something with the submitted form'

    return render(request, "oauth/oauth_register.html", locals())
