from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# Fix for TypeError: OAuth2Client.__init__() got multiple values for argument 'scope_delimiter'
class MyOAuth2Client(OAuth2Client):
    def __init__(self, *args, **kwargs):
        if 'scope_delimiter' in kwargs:
            del kwargs['scope_delimiter']
        super().__init__(*args, **kwargs)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/oauth/callback/google" 
    client_class = MyOAuth2Client

class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    callback_url = "http://localhost:3000/oauth/callback/naver"
    client_class = MyOAuth2Client

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = "http://localhost:3000/oauth/callback/kakao"
    client_class = MyOAuth2Client