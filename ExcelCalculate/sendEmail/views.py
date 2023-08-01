from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def send(receiverEmail, verifyCode):
    # receiverEmail : 회원가입 때 입력한 이메일
    # verifyCode : 인증코드
    print(receiverEmail, verifyCode)
    try:
        content = {'verifyCode' : verifyCode}
            # content 변수에 인증코드를 딕셔너리 형태로 담아준다.
        msg_html = render_to_string("sendEmail/email_format.html", content)
            # 미리 작성한 email_format.html에 인증코드가 담긴 content를 전달하여 
            # msg_html에 HTML형식의 이메일 내용을 담아준다.
        msg = EmailMessage(subject ="멀티캠퍼스 인증 코드 발송 메일",
                           body=msg_html,
                           from_email="multicampus28@gmail.com",
                           bcc=[receiverEmail])
            # EmailMessage 함수로 msg라는 이메일 객체를 생성하고 다음의 인자들을 지정합니다.
            # subject : 이메일제목
            # body : 이메일내용
            # from_email : 발신자 이메일 주소
            # bcc : 수신자를 설정하고 다른이들이 볼 수 없게 숨겨준다.
        msg.content_subtype='html'
            # 이메일 내용의 형식을 html로 설정한다.
        msg.send()
            # msg 이메일 객체를 발송해준다.
        print("sendEmail > views.py > send 함수 임무 완료----------")
        return True
    except:
        print("sendEmail > views.py > send 함수 임무 실패----------")
        return False
        # 인증코드 발송은 에러 날 가능성 존재
        # Google 이용 <--- 개발자가 통제 불가능하므로 try-except 사용