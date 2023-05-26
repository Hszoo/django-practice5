from django import forms
from .models import Post
# 폼을 정의해서 뷰-> html 동적으로 html폼태그 다룰 수 있음

# 사용자가 전달한 데이터의 양식을 지정하는 게 폼 
# ㄴ 데이터를 저장하는 건 모델 

# #방식1)
# class PostBaseForm(forms.Form) :
#     image = forms.ImageField(label='이미지')
#     # content = forms.CharField()
#     # 입력받는 형태를 textarea로 넓어지게 할 수 있음 (위젯사용)
#     content = forms.CharField(label='내용', widget=forms.Textarea, required=True)
#     CATEGORY_CHOICES = [
#         ('1', '일반'),
#         ('2', '계정'),
#     ]
#     category = forms.ChoiceField(label='카테고리',choices=CATEGORY_CHOICES)
#     # label 은 verbose_name 처럼 


#방식2)
class PostBaseForm(forms.ModelForm) :
    class Meta : # meta클래스 상속받음 
        model = Post
        fields = '__all__'
        # 모델폼 상속받고, 모델=Post 모델로 지정, 필드 전체 지정 -> 방식1과 같은 동작, 더 간편 

from django.core.exceptions import ValidationError
class PostCreateForm(PostBaseForm) :
    class Meta(PostBaseForm.Meta): 
        fields = ['image', 'content']

# clean 언더바 필드명 -> 유효성 검사하는 함수가 됨 와 신기하다
    def clean_content(self) : # '비속어' 포함하는 게시글 작성 불가 
        data = self.cleaned_data['content']
        if "비속어" == data :
            raise ValidationError("비속하는 사용하지 마세요")
        return data

class PostUpdateForm(PostBaseForm) :
    class Meta(PostBaseForm.Meta): 
        feilds = ['image', 'content']

class PostDetailForm(PostBaseForm) : # ???????이거 뭔.. 
    # 설명 똑바로 안함 심지어 자기가 하다가 에러 계속 냄 뭐하는 
    def __init(self, *args, **kwargs) : # 왜 쓴거냐 
        super(PostDetailForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['disabled'] = True