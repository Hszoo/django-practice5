from django.contrib import admin
from django.conf import settings # settings 파일에 있는 값들을 가져올 수 있음 
from django.conf.urls.static import static 
from django.urls import path, include
from posts.views import index, url_view, url_parameter_view, function_view, function_view_list, class_view

urlpatterns = [  #이것도 리스트이니까 마지막에 콤마 꼭 찍기
    path('admin/', admin.site.urls),
    path('url/', url_view),
    path('url/<str:username>/', url_parameter_view),
    # urlpattern 에서 ㄴ 변수로 지정해 놓음 views에서 받아서 쓸 수 있다. 
    # url/문자아무거나 와도 실행됨 url_parameter_view 함수가 실행됨
    path('fbv/list/', function_view_list),
    path('fbv/', function_view),
    path('cbv/', class_view.as_view()), #class_view는 클래스라 as_view로 실행해줘야됨
    path('', index, name='index'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('__debug__', include('debug_toolbar.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)