from django.shortcuts import render, redirect
# 장고에서 제공하는 폼을 이용한 회원가입폼 
from django.contrib.auth import login, logout # 장고에서 로그인,아웃함수제공
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserCreateForm, SignUpForm
from users.models import User
# Create your views here.
def signup_view(request) :
    if request.method =='GET' :
        form = SignUpForm
        context = {'form' : form}
        return render(request, 'accounts/signup.html', context)
    else : #POST
        form = SignUpForm(request.POST)
        if form.is_valid() :
            instance = form.save()
            return redirect('index')
        else :
            return redirect('accounts:signup')
        
def login_view(request) :
    if request.method == 'GET' : # GET, 로그인 폼 응답 
        return render(request, 'accounts/login.html', {'form':AuthenticationForm})
    else :
        form = AuthenticationForm(request, data=request.POST)

        # 폼 유효성 검사 
        if form.is_valid() :
            # 비지니스 로직 처리 - 로그인 처리
            login(request, form.user_cache) #로그인처리하는 함수
            # 응답
            return redirect('index')
        else :
            # 비지니스 로직 처리 - 로그인 실패 

            # 응답 폼을 넘겨주면 데이터(사용자가 입력한), 에러메시지(어떤 걸 잘못입력해서 로그인이 안되는지) 출력됨
            return render(request, 'accounts/login.html', {'form':form}) 
        #if username == '' or username == 'None':
        #    pass
        #if username == '' :
        #    pass
        
        #user = User.objects.get(username=username)
        #if user == None :
        #    pass
        #request.POST.get('username')

def logout_view(request) :
    #form = 
    if request.user.is_authenticated :
        logout(request)

    #if form.is_valid() :
    return redirect('index')