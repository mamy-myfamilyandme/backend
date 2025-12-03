from django.urls import path
from .views import GoogleLogin, NaverLogin, KakaoLogin, kakao_callback

urlpatterns = [
    #  access_token을 http://localhost:8000/api/auth/google/로 POST 요청 보내면,
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("naver/", NaverLogin.as_view(), name="naver_login"),
    path("kakao/", KakaoLogin.as_view(), name="kakao_login"),
    path("kakao/callback/", kakao_callback, name="kakao_callback"),
]
