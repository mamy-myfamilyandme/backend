from django.urls import path
from .views import GoogleLogin

urlpatterns = [
    #  access_token을 http://localhost:8000/api/auth/google/로 POST 요청 보내면,
    path("google/", GoogleLogin.as_view(), name="google_login"),
]
