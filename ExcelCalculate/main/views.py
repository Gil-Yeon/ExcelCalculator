from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def signup(request):
    return render(request, 'main/signup.html')

def join(request):
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
        # User DB의 속성을 활용하여 user 변수에 할당
    user.save()
    print('사용자 정보 저장 완료')

    return redirect('main_verifyCode')
        # url의 name='main_verifyCode'태그를 이용해 MVC패턴에 따른다.

def signin(request):
    return render(request, 'main/signin.html')

def verifyCode(request):
    return render(request, 'main/verifyCode.html')

def verify(request):
    return redirect('main_index') # 인증후에는 메인화면으로 보내줌.

def result(request):
    return render(request, 'main/result.html')