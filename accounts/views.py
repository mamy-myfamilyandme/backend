from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/api/auth/google/callback/" 
    client_class = OAuth2Client

class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    callback_url = "http://localhost:8000/api/auth/naver/callback/"
    client_class = OAuth2Client


