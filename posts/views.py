from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic.list import ListView # cbv 에서 listView쓰기 위해 받아옴
from django.contrib.auth.decorators import login_required
from .models import Post # posts 앱 내(현재 views와 같은 경로상의) models 받아오기
from .forms import PostBaseForm, PostCreateForm, PostDetailForm
# Create your views here.

def index(request) :
    post_list = Post.objects.all().order_by('-create_at') # post 모델에 있는 모든 데이터 가져와라
    context = {
        'post_list' : post_list, 
    }
    return render(request, 'index.html', context)

def post_list_view(request) :
    post_list = Post.objects.all() # post 모델에 있는 모든 데이터 가져와라
    #post_list = Post.objects.filter(writer=request.user) # 모델 내 writer 가 현재 로그인한 사용자와 같은지 조회 
    context = {
        'post_list' : post_list, 
    }
    return render(request, 'posts/post_list.html', context) # BASE-DIR로 위에 위에 즉 워크스페이스 / templates까지 지정해줬으니까 그 이하를 지정해주면 됨 

def post_detail_view(request, id) :
    try:
        post = Post.objects.get(id=id) # 더보기 페이지에서 url 템플릿으로 먹이려면, id값도 넘겨줘야할텐데 그떄 id넘기기 위해서는 여기 context 넘겨줘야됨.. 
    # 존재하지 않는 페이지 입력받아 예외발생하면 
    except Post.DoesNotExist:
        return redirect('index') # 홈으로 redirect 
    context = {
        'post' : post,
        'form' : PostDetailForm(),
    }
    return render(request, 'posts/post_detail.html', context)

@login_required # 아래 함수실행 전에 실행되어, 로그인 상태에서만 아래 함수가 실행 되도록  
def post_create_view(request) :
    if request.method == 'GET' :
        return render(request, 'posts/post_form.html')
    else :
        image = request.FILES.get('image')
        content = request.POST.get('content')
        print(image)
        print(content)

        # 사용자가 입력한 file과 content data 객체로 추가하기 
        Post.objects.create(
            image=image,
            content=content,
            #writer=request.user
        )
        return redirect('index')
    
def post_create_form_view(request) :
    if request.method == 'GET' :
        form = PostCreateForm() # GET으로 폼 제공시에는 인수 없음 
        context = {'form' : form}
        return render(request, 'posts/post_form2.html', context)
    
    else :
        form = PostCreateForm(request.POST, request.FILES) # POST로 사용자가 입력한 데이터를 가져와 \
        if form.is_valid() : # 장고 폼에서 데이터들이 적합한지 판단할 수 있음  
            Post.objects.create( # 적합하다면 각각을 저장한다. 
            # cleaned_data : 폼에 작성된 필드 타입 기반으로, 각 데이터가 유효성 검사를 거치게 됨 
                image=form.cleaned_data['image'],
                content=form.cleaned_data['content'],
                writer=request.user
        )
        else :
            return redirect('posts:post-create') # 유효성 검사 실패하면 다시 폼으로 넘어가게 
        return redirect('index')

@login_required
def post_update_view(request, id) : # url 패턴에 <int:id> 해놔서 id값 가져오기 가능 / urls에서 이거 안해놓으면 당연히 못가져오겠져    
    #post = get_object_or_404(Post, id=id, writer=request.user) writer로 받는 값이 없어도 에러 발생시키는 구문 # 모델, id prameter
    post = Post.objects.get(id = id) # 특정 id값의 post 객체를 받음 

    if request.user != post.writer :
        raise Http404('잘못된 접근입니다.') # 로그인한 사용자와 작성자가 다르면 에러 
    
    if request.method == 'GET' :
        context = { 'post':post }
        return render(request, 'posts/post_form.html', context)
    elif request.method == 'POST' :
        new_image = request.FILES.get('image')
        content = request.POST.get('content')
        print(new_image)
        print(content)

        if new_image : 
            post.image.delete() #기존의 이미지는 삭제해서 중복된 이미지 쌓이지 않도록 
            post.image = new_image # 수정된 이미지와 content로 변경 
        post.content = content 
        post.save()
        return redirect('posts:post-detail', post.id)

@login_required
def post_delete_view(request, id) :
    
    post = get_object_or_404(Post, id=id) # 모델, id prameter
    if request.user != post.writer :
        raise Http404('잘못된 접근입니다.') # 로그인한 사용자와 작성자가 다르면 에러 
    
    if request.method == 'GET':
        context = {'post' : post}
        return render(request, 'posts/post_confirm_delete.html', context)
    else:
        post.delete()
        return render('index')

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
