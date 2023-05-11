from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# 장고에서 알아서 생성한 user 테이블 가져와서 사용 함 


# Create your models here.

# 여기에 작성한게 데이터베이스로 만들어짐 
class Post(models.Model): # Model클래스 상속 받아서, model이라는 객체로 받아서 사용한다. 
    image = models.ImageField(verbose_name='이미지', null=True, blank=True) # 필드의 이름을 verbosename으로 지정 
    # null : db에 null 값 들어가는 것 허용할 건지 
    content = models.TextField(verbose_name='내용') # 긴 데이터 작성 가능 
    create_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True) # 현재 날짜 자동 추가하도록 
    view_count = models.IntegerField(verbose_name='조회수', default=0)
    # 사용자 1 : 게시글 (다) 의 관계라고 했음, 
    # 사용자를 참조하도록 다에 속하는 테이블에서 FK 지정해주면 된다. 필수
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

# 댓글에 해당하는 model 정의 
class Comment(models.Model) : 
    content = models.TextField(verbose_name='내용')
    create_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE) # FK 지정, Post 테이블을 참조할 /
    #on_delete : Comment 테이블이 참조하는 Post 테이블 삭제할 때 관련 데이터 다 삭제 하도록 속성 CASCADE 지정 
    # ㄴ 게시글 삭제하면 댓글도 당연히 다 삭제해야 하니까 
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE) # 작성자 = 사용자, 사용자 모델을 참조하면 됨 / user 모델을 장고가 알아서 생성 
    # 어떻게 가져오냐? import get_user_model import해서 사용 






