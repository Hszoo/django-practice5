from django.contrib import admin
from .models import Post, Comment 
# import 하는 경로는 상대경로로 .models -> post 내의 models 파일 의미 
# Register your models here.

# 아래에 등록한 model들이 admin페이지의 왼쪽에 나오면서 관리자 페이지에서 CRUD 기본 접근할 수 있게 된다. 
# admin.site.register(-- 인수 : 등록할 모델명 -- ) 

class CommnetInline(admin.TabularInline) : # TabularInline을 상속받아서 특정 Post에서 Comment도 뜰 수 있도록 
                                        # StackedInline 댓글창에 표시되는 작성자.. 뭐 이런것들이 세로로 배치됨 위에 클래스랑 비슷한데 배치가 다를 뿐 
    model = Comment # model 값을 import 한 Comment 값으로 넣어준다. 
    extra = 3 # 댓글창이 기본 5개도록 설정 
    min_num = 3 # 댓글 창이 최소 3개는 존재하도록 제한 
    max_num = 5 # 댓글 창 최대 5개까지만 추가되도록 제한 
    verbose_name = '댓글' # 댓글 창이 나오는 곳의 이름 지정 가능 
    verbose_name_plural = '댓글' # 복수개의 댓글 창인 경우에 이름 따로 지정 가능 
# 이런식으로 admin 파일에서 admin 페이지의 UI구성할 수 있음 


@admin.register(Post) 
class PostModelAdmin(admin.ModelAdmin) :
    list_display = ('id', 'content', 'image', 'create_at', 'view_count', 'writer')
    # admin 에서 post 로 들어가면 id와 content로 구분해서 보이도록 함 
    # list_display로 지정가능한 건 post 모델에 정의한 필드들 
    
    # list_editable : 인수로 들어간 필드를 어드민 페이지에서 수정할 수 있게함 
    list_editable = ('content',)  
    list_filter = ('create_at',) # 필터의 카테고리가 생긴다. / 하나를 특정하기 위해 필터 설정하는 거 
    search_fields = ('id', 'writer__username', ) # 인수로 넣어준 값으로 검색이 가능하고 여러개의 데이터 특정할 수도 있음 
    ## writer는 user 모델을 참조하는 앤데, 얘에다가 __username 해주면 작성자의 이름으로 검색이 가능해진다. 
    search_help_text = '게시판 번호, 작성자 검색이 가능합니다. ' # 뭐 이런식으로 UI구성할 수 있음 
    readonly_fields = ('create_at', ) # create_at  auto_now_add=True로 날짜가 자동으로 설정되도록 해서 admin에서는 별도 지정 불가능함 
    # 그래서 admin에서는 안 뜰 텐데 readonly_field는 이 값을 수정 불가능하도록 하여 띄워줄 수 있다. 
    # 그 밖에도 관리자 페이지에서 별도록 수정 불가능하도록 하고 싶은 모델의 필드 값들을 넣어주면 admin페이지에서는 수정이 안된다. 
    inlines = [CommnetInline] #위의 클래스에서 model값에 import 받은 Comment값을 넣어줬고, Post모델설정에서(여기클래스) inline으로 추가해줬음 
    # 이제 게시글에 들어가서도 comment 댓글들 볼 수 있음 
    
    actions = ['make_published']

    def make_published(modeladmin, request, queryset) : 
        for item in queryset :
            item.content = '운영 규정 위반으로 인한 게시글 삭제 처리.'
            item.save()