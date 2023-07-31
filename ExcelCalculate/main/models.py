from django.db import models

# Create your models here.
class User(models.Model):
    user_name     = models.CharField(max_length=20)
    user_email    = models.EmailField(unique=True)
        # 사용자 이메일은 고유해야 하므로 unique로 설정
    user_password = models.CharField(max_length=100)
    user_validate = models.BooleanField(default=False)
        # default False로 설정하여 초기 User데이터 생성 시 인증이 필요하도록 함