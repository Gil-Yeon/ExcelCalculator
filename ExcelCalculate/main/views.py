from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from random import *
from sendEmail.views import *

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def signup(request):
    return render(request, 'main/signup.html')

def join(request):
    print('테스트', request)

    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
        # User DB의 속성을 활용하여 user 변수에 할당
    user.save()
    print('사용자 정보 저장 완료')

    # 인증코드 하나 생성
    code = randint(1000, 9000)
        # 서버가 보낸 코드, 쿠키와 세션
    print("인증코드 생성----------", code)

    # 응답 객체 생성
    response = redirect("main_verifyCode")
        # 사용자를 main_verifyCode로 리디렉션 시키는 응답객체 response를 생성한다.
    response.set_cookie('code', code)
        # 인증코드를 response에 'code'라는 이름의 쿠키로 생성한다. 이 쿠키는 사용자의 인증 상태를 나타내는 값으로 활용
    response.set_cookie('user_id', user.id)
        # user id를 response에 'user_id'라는 이름의 쿠키로 생성한다. 이 쿠키로 사용자를 식별한다.
    print("응답 객체 완성--------", response)

    # 이메일 발송 하는 함수 만들기
    send_result = send(email, code)
        # sendEmail > view.py에 있는 send함수를 실행시켜 send_result에 할당해준다.
    if send_result:
        print("Main > views.py > 이메일 발송 중 완료된 거 같음....")
        return response
            # 정상적으로 send함수가 실행되면
			# response로 인해 사용자는 main_verifyCode로 리디렉션 된다.
    else:
        return HttpResponse("이메일 발송 실패!")

def signin(request):
    return render(request, 'main/signin.html')

def verifyCode(request):
    return render(request, 'main/verifyCode.html')

def verify(request):
    user_code = request.POST['verifyCode']
        # 사용자가 입력한 code값을 user_code에 할당
    cookie_code = request.COOKIES.get('code')
        # 쿠키에서 이름이 'code'로 저장되어 있는 쿠키값(join함수에서 저장했던 쿠키)
        # 을 가져와 cookie_code에 할당한다.
    print(user_code, cookie_code)
    
    if user_code == cookie_code:
        # 사용자가 입력한 인증코드와 join함수에서 생성됐던 인증코드를 비교합니다.
        user = User.objects.get(id=request.COOKIES.get('user_id'))
            # 쿠키에 'user_id'로 저장된 사용자 id를 이용하여 해당 사용자의
            # User 모델 데이터를 user변수에 할당한다.
        user.user_validate = 1
            # True = 1 False = 0임을 이용해서 사용자인증이 True임을 선언
        user.save()

        print("DB에 user_validate 업데이트------------------")
        
        response = redirect('main_index')
            # 인증이 완료되면 사용자를 main_index으로 리디렉션 시키는 응답 객체를 생성
        response.delete_cookie('code')
        response.delete_cookie('user_id')
            # 저장되어 있는 쿠키를 삭제
        response.set_cookie('user', user)
            # user 객체를 response에 'user'라는 이름의 쿠키에 생성한다. 이 쿠키는 추후 인증이 필요한 경우 사용된다.

        # 사용자 정보를 세션에 저장
        # request.session['user_name'] = user.user_name
        # request.session['user_email'] = user.user_email
            # user의 name과 email값을 세션에 할당한다.
        return response
            # 메인페이지로 리디렉션한다.

    else:
        print("False")
        return redirect('main_index')
            # 메인페이지로 리디렉션한다.

def result(request):
    return render(request, 'main/result.html')