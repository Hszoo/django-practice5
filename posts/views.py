from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView # cbv 에서 listView쓰기 위해 받아옴
from .models import Post # posts 앱 내(현재 views와 같은 경로상의) models 받아오기
# Create your views here.

def index(request) :
    return render(request, 'index.html')
def post_list_view(request) :
    return render(request, 'posts/post_list.html') # BASE-DIR로 위에 위에 즉 워크스페이스 / templates까지 지정해줬으니까 그 이하를 지정해주면 됨 
def post_detail_view(request, id) :
    return render(request, 'posts/post_detail.html')
def post_create_view(request, id) :
    return render(request, 'posts/post_form.html')
def post_update_view(request, id) :
    return render(request, 'posts/post_form.html')
def post_delete_view(request, id) :
    return render(request, 'posts/post_delete.html')

def url_view(request) :
    print('url_view 함수 실행중 ')
    data = {'code' : '001' , 'msg' : 'OK'}
    return JsonResponse(data)
    # 
    # return HttpResponse('<h1>url_view</h1>') 
    # 텍스트로 응답함      ㄴ html text로 먹음 

# 뷰에서 url로 데이터 넘겨주기  
def url_parameter_view(request, username) :
    print("url_parameter_view 실행중 ")
    print(f'username : {username}')
    print(f'request.GET : {request.GET}') # 쿼리 str을 받을 수도 있다.
    # 넘겨주는 형태 : /?키=value&여러개=앤드기호로
    # ㄴ 딕셔너리 형태로 저장된다. 
    return HttpResponse(username)

def function_view(request) :
    method = request.method
    print(f'request.method:{request.method}')
    #if문으로 분기처리 -> get일땐 get출력/ post일땐 post
    # 예를 들어, 회원가입 폼받을 때는 GET 회원가입 자체 할 때는 POST 
    if( request.method == 'GET') :
        print(f'request.GET : {request.GET}')
    elif request.method == 'POST':
        print(f'request.POST:{request.POST}')
    return render(request, 'view.html')

### 여기까지 함수 기반뷰 FBV

### 여기서부터 클래스 기반뷰 CBV
class class_view(ListView) : # 매개변수 listView는 import 해줘야 사용 가능 
    model = Post
    template_name = 'cbv_view.html'

# 위의 cbv를 fbv로 작성하는 방법 
def function_view_list(request) :
    object_list = Post.objects.all().order_by('-id')
    return render(request, 'cbv_view.html', {'object List' : object_list})
    