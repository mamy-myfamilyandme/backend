from django.http import HttpResponse
from django.shortcuts import redirect, render

def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, 'index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return HttpResponse(f"<h1>환영합니다! {request.user}님 👋</h1><p>로그인 성공 페이지입니다.</p><a href='/accounts/logout/'>로그아웃</a>")
