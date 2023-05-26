from django.db import models
from django.contrib.auth.models import UserManager as DjangoUserManager, AbstractUser # 장고 안.. 에 있는 Users 모델

# 매니저가 뭐냐면 Post.objects..... 이렇게 사용했던 것들을 매니저라고 한다
# 모델이 db로 쿼리를 날릴때 제공해주는 인터페이스? 
class UserManager(DjangoUserManager) :
    # 언더바로 시작하는 함수 : 외부로 부터 숨기고 싶을 때
    # **extra_fields : 그 외 나머지 필드들 
    def _create_user(self, username, email, password, **extra_fields):
        if not email :
            raise ValueError('이메일은 필수 입력 값입니다. ')
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) # 사용자 비밀번호를 해싱(암호화)해서 db에 보관 
        user.save()

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password,  **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password,  **extra_fields)


# 이미 있던 User 모델을 커스텀함 
# >> settings.py 에서 AUTH_USER_MODEL = 'users.User' 내가 만든 모델로 바꿔주기 
class User(AbstractUser) : # AbstractUsers 상속받음 << 여기 안에 많은 필드들 정의 돼 있음 
    # 따로 정의 안해도 그 필드들이 ... 뭔지 알지
    phone = models.CharField(verbose_name='전화번호', max_length=11)
    #주로 꼭 들어가야 하는 데이터는 User모델 커스텀해서 사용함 , 그렇지 않은 건 확장으로 아래 모델처럼 빼요

    objects = UserManager() # 매니저를 커스텀했으면 적용해줘야됨 

# #데이터 확장
# class UserInfo(models.Model) :
#     phone_sub = models.CharField(verbose_name='보조 전화번호', max_length=11)
#     user = models.ForeignKey(to='User', on_delete=models.CASCADE)