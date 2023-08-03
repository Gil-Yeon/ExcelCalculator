from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from random import *
from sendEmail.views import *

# Create your views here.
def index(request):
    if 'user_name' in request.session.keys():
        # 정상적으로 login 함수를 거쳤다면 request.session['user_name']을 통해
        # 'user_name'이 session에 존재할 것이므로 조건문 실행
        return render(request, 'main/index.html')
            # 사용자의 세션 정보가 담겨져 있는 상태의 index.html을 화면에 표시
    else:
        return redirect('main_signin')
            # login 되지 않은 상태이기 때문에 다시 로그인 화면으로 리디렉션
    
    # return render(request, 'main/index.html')
        # 세션 정보가 없는 index.html

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

def login(request):
    # 로그인된 사용자만 이용할 수 있도록 구현
    # 이 때, 현재 사용자가 로그인된 사용자인지 판단하기 위해 세션 사용(verify에서 만든 세션)
    # 세션 처리 진행

    loginEmail = request.POST['loginEmail']
    loginPW = request.POST['loginPW']
    	# 사용자 요청으로부터 email과 pw를 가져와 변수에 할당한다.

    try:
        user = User.objects.get(user_email=loginEmail)
    	# User 모델에서 입력한 이메일(loginEmail)과 같은 이메일을 가진 유저 데이터를 가져와 user에 할당한다.
    except:
        return redirect("main_loginFail")
    
    if user.user_password == loginPW:
    	# 모델에서 가져온 pw와 입력한 패스워드(loginPW)가 서로 같다면 실행
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        	# 해당 유저의 이름과 이메일을 세션에 저장하여 로그인한 상태로 처리한다.
        return redirect('main_index')
        	# 메인 인덱스로 리디렉션 시킨다.
    else:
        # 로그인 실패, 정보가 다름
        return redirect("main_loginFail")
        	# loginFail로 리디렉션 시킨다.

def loginFail(request):
    return render(request, 'main/loginFail.html')
        # loginFail.html을 화면에 띄워준다.

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
        # response.set_cookie('user', user)
            # user 객체를 response에 'user'라는 이름의 쿠키에 생성한다. 이 쿠키는 추후 인증이 필요한 경우 사용된다.

        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
            # user의 name과 email값을 세션에 할당한다.

        return response
            # 메인페이지로 리디렉션한다.

    else:
        print("False")
        return redirect('main_index')
            # 메인페이지로 리디렉션한다.

def result(request):
    if 'user_name' in request.session.keys():
        # 로그인 했으므로 user_name, user_email 세션이 존재
        # calculate에서 요청한 grade_calculate_dic, email_domain_dic 세션이 존재
        content = {}
        content['grade_calculate_dic'] = request.session['grade_calculate_dic']
        content['email_domain_dic'] = request.session['email_domain_dic']
            # 보안 문제로 calculate에서 요청한 세션을 새로운 객체에 저장

        del request.session['grade_calculate_dic']
        del request.session['email_domain_dic']
            # calculate에서 저장한 기존 세션 삭제

        return render(request, 'main/result.html', content)
            # 사용자의 세션 정보가 content에 담겨 있는 상태에서 main > result.html을 띄워준다. 
    else:
        return redirect('main_signin')

def logout(request):
    del request.session['user_name']
    del request.session['user_email']
    # 세션정보를 삭제하는 것으로 로그인 상태를 해제한다.

    return redirect('main_signin')