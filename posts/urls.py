from django.urls import path
from .views import post_list_view, post_create_view, post_create_form_view, post_update_view, post_detail_view, post_delete_view

app_name='posts'

urlpatterns = [
    path('',post_list_view, name="post-list"), # 여기 이름을 index.html에서 가져다 쓸 수 있음 -> templates 언어 
    #path('new/',post_create_view, name='post-create'),
    path('new/',post_create_form_view, name='post-create'),
    path('<int:id>/',post_detail_view, name='post-detail'), # 모델의 id값 의 detail화면 보여줌 
    path('<int:id>/edit/',post_update_view, name='post-update'), # id의 수정 -> 업데이트 화면 보여줌 
    path('<int:id>/delete/',post_delete_view, name='post-delete'), # id의 delete -> delete 화면 보여줌 
]