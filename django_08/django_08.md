# Django 08



## Django CRUD

> Django : 파이썬 기반 웹 프레임워크



### 1. 환경 설정

#### 1-1. 가상환경 생성 및 실행

> 가상환경 : 프로젝트별 별도 패키지 관리

```bash
# 가상환경 생성
$ python -m venv pjt-venv

# 가상환경 폴더 생성 확인
$ ls

# 가상환경 실행
$ source pjt-venv/Scripts/activate
(pjt-venv)
```

#### 1-2. Django 설치 및 기록

> 가상환경 실행한 상태에서 패키지 설치

```bash
# Django LTS 버전 설치
$ pip install django==3.2.13

# black 패키지 설치
$ pip install black

# 패키지 설치 확인
$ pip list

# 패키지 기록
$ pip freeze > requirements.txt
```

#### 1-3. Django 프로젝트 생성

```bash
# Django 프로젝트 생성
$ django-admin startproject pjt .

# 프로젝트 폴더 생성 확인
$ ls
```

#### 1-4. 기타

```bash
# 서버 정상 실행 확인
$ python manage.py runserver
# ctrl + c 눌러서 종료

# VS code 실행
$ code .
```



### 2. Django App

#### 2-1. App 생성

```bash
# Django 앱 생성
python manage.py startapp articles
```

#### 2-2. App 등록

- `pjt/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'articles',
    ...
]
```

#### 2-3. URL 설정

> app 단위의 URL 관리

- `pjt/urls.py` 파일에 추가

```python
...
from django.urls import path, include

urlpatterns = [
    ...
    path('articles/', include('articles.urls')),
]
```

- `articles/urls.py` 파일 생성

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # http://127.0.0.1:8000/articles/
    path('', views.index, name='index'),
    ...
]
```

- 활용 : `articles:index` -> `/articles/`

  - Template에서 활용 예시

  ```html
  {% url 'articles:index' %}
  ```

  - View에서 활용 예시

  ```python
  redirect('articles:index')
  ```

#### 2-4. View 설정

- `articles/views.py` 파일에 함수 생성

```python
from django.shortcuts import render, redirect

def index(request):
    ...
    return render(request, 'articles/index.html')
```

#### 2-5 Template 설정

- `articles/templates/articles` 폴더 생성 후, 템플릿 관리
- `articles/index.html` 파일 생성



### 3. Model 정의

> DB 스키마 설계

#### 3-1. 클래스 정의

- `articles/models.py` 파일에 클래스 추가

```python
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### 3-2. 마이그레이션 파일 생성

- `articles/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

#### 3-3. DB 반영

```bash
$ python manage.py migrate
```

#### 3-4 Model 활용

- `articles/views.py` 파일에 임포트 추가

```python
from django.shortcuts import render, redirect
from .models import Article
...
```



### 4. CRUD 기능 구현

#### 4-0. ModelForm 선언

> 선언된 모델에 따른 필드 구성 (1) Form 생성 (2) 유효성 검사

- `articles/forms.py` 파일 생성

```py
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'content']
```

#### 4-1 게시글 생성

> 기존 new, create -> ModelForm 로직 create로 변경
>
> 생성 버튼 누르면 게시글 생성 페이지로 이동

##### (1) HTML Form 제공 (GET)

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # http://127.0.0.1:8000/articles/
    path('', views.index, name='index'),
    # http://127.0.0.1:8000/articles/create/
    path('create/', views.create, name='create'),
    ...
]
```

- `articles/views.py` 파일에 임포트 추가 및 함수 생성

```python
...
from .forms import ArticleForm
...

def create(request):
    # ModelForm
    article_form = ArticleForm()
    # template에 전달
    context = {
        'article_form': article_form
    }
    # 게시글 생성 페이지로 이동
    return render(request, 'articles/create.html', context=context)
```

- `articles/index.html` 파일에 추가

```html
<a href="{% url 'articles:create' %}">글 쓰기</a>
```

- `articles/create.html` 파일 생성
  - HTML Form 태그 활용 : 어떤 필드로 구성할 것인가(`name`, `value`) / 어디로 보낼 것인가(`action`, `method`)

```html
<h1>글 쓰기</h1>
<form action="" method="POST">
  <!-- POST 요청에서 CSRF 공격 방어 : 전송된 token의 유효성 검증 -->
  {% csrf_token %}
  <!-- ModleForm -->
  {{ article_form.as_p }}
  <input type="submit" value="글 쓰기">
</form>
```

##### (2) 입력받은 데이터 처리 (POST)

> 게시글 DB에 생성하고 index 페이지로 redirect

- `articles/views.py` 파일의 함수로 요청 처리

```python
def create(request):
    # POST 요청 처리
    if request.method == 'POST':
        # ModelForm에서 입력받은 데이터
        article_form = ArticleForm(request.POST)
        # 유효성 검사를 통과하면
        if article_form.is_valid():
            # DB에 저장
            article_form.save()
            # index 페이지 redirect
            return redirect('articles:index')
    # GET 요청 처리
    else: 
        article_form = ArticleForm()
    # template에 전달
    context = {
        'article_form': article_form
    }
    # 게시글 생성 페이지로 이동
    return render(request, 'articles/create.html', context=context)
```



#### 4-2 게시글 목록

> DB에서 게시글을 가져와서, template에 전달

- `articles/views.py` 파일의 함수로 요청 처리

```python
def index(request):
    # DB에서 게시글 가져옴 + pk의 내림차순으로 정렬
    articles = Article.objects.order_by('-pk')
    # template에 전달
    context = {
        'articles': articles
    }
    # 게시글 목록 페이지로 이동
    return render(request, 'articles/index.html', context)
```

- `articles/index.html` 파일에 추가

```html
<h1>글 목록</h1>
{% for article in articles %}
<h3>{{ article.title }}</h3>
<p>{{ article.created_at }} | {{ article.updated_at }}</p>
<hr>
{% endfor %}
```



#### 4-3 게시글 상세보기

> 게시글 목록에서 특정 게시글의 제목을 누르면 상세보기 페이지로 이동

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # http://127.0.0.1:8000/articles/
    path('', views.index, name='index'),
    # http://127.0.0.1:8000/articles/create/
    path('create/', views.create, name='create'),
    # http://127.0.0.1:8000/articles/int:pk/
    path('<int:pk>', views.detail, name='detail'),
    ...
]
```

- `articles/views.py` 파일의 함수로 요청 처리

```python
def detail(request, pk):
    # DB에서 특정 게시글 하나만 가져옴
    article = Article.objects.get(pk=pk)
    # template에 전달
    context = {
        'article': article
    }
	# 게시글 상세보기 페이지로 이동
    return render(request, 'articles/detail.html', context)
```

- `articles/index.html` 파일에 추가

```html
<h1>글 목록</h1>
{% for article in articles %}
<!-- <a> 태그로 제목에 링크 설정, 해당 게시글의 pk를 전달 -->
<h3><a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a></h3>
<p>{{ article.created_at }} | {{ article.updated_at }}</p>
<hr>
{% endfor %}
```

- `articles/detail.html` 파일 생성

```html
<h1>{{ article.pk }}번 게시글</h1>
<p>{{ article.created_at }} | {{ article.updated_at }}</p>
<p>{{ article.content }} </p>
```



#### 4-4 게시글 삭제

> 삭제 버튼을 누르면 해당 게시글 삭제

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # http://127.0.0.1:8000/articles/
    path('', views.index, name='index'),
    # http://127.0.0.1:8000/articles/create/
    path('create/', views.create, name='create'),
    # http://127.0.0.1:8000/articles/int:pk/
    path('<int:pk>', views.detail, name='detail'),
    # http://127.0.0.1:8000/articles/int:pk/delete/
    path('<int:pk>/delete/', views.delete, name='delete'),
    ...
]
```

- `articles/views.py` 파일의 함수로 요청 처리

```python
def delete(request, pk):
    # DB에서 특정 게시글 하나만 가져옴
    article = Article.objects.get(pk=pk)
    # 게시글 삭제
    article.delete()
	# index 페이지 redirect
    return redirect('articles:index')
```

- `articles/index.html` 파일에 추가

```html
<a href="{% url 'articles:delete' article.pk %}">글 삭제</a>
```

#### 4-5 게시글 수정

> 수정 버튼을 누르면 특정 게시글의 수정 페이지로 이동

##### (1) HTML Form 제공 (GET)

> 사용자에게 수정할 수 있는 양식 제공

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # http://127.0.0.1:8000/articles/
    path('', views.index, name='index'),
    # http://127.0.0.1:8000/articles/create/
    path('create/', views.create, name='create'),
    # http://127.0.0.1:8000/articles/int:pk/
    path('<int:pk>', views.detail, name='detail'),
    # http://127.0.0.1:8000/articles/int:pk/delete/
    path('<int:pk>/delete/', views.delete, name='delete'),
    # http://127.0.0.1:8000/articles/int:pk/update/
    path('<int:pk>/update/', views.update, name='update'),
]
```

- `articles/views.py` 파일에 임포트 추가 및 함수 생성

```python
def update(request, pk):
    # DB에서 특정 게시글 하나만 가져옴
    article = Article.objects.get(pk=pk)
    # 특정 게시글의 데이터를 form에 입력
    article_form = ArticleForm(instance=article)
    # template에 전달
    context = {
        'article_form': article_form
    }
	# 게시글 수정 페이지로 이동
    return render(request, 'articles/update.html', context)
```

- `articles/update.html` 파일 생성
  - HTML Form 태그 활용 : 어떤 필드로 구성할 것인가(`name`, `value`) / 어디로 보낼 것인가(`action`, `method`)

```html
<h1>글 수정</h1>
<form action="" method="POST">
  <!-- POST 요청에서 CSRF 공격 방어 : 전송된 token의 유효성 검증 -->
  {% csrf_token %}
  <!-- ModleForm -->
  {{ article_form.as_p }}
  <input type="submit" value="글 수정">
</form>
```

##### (2) 입력받은 데이터 처리 (POST)

> 기존 edit, update -> ModelForm 로직 update로 변경
>
> 특정 게시글 수정고 index 페이지로 redirect

- `articles/views.py` 파일의 함수로 요청 처리

```python
def update(request, pk):
    # DB에서 특정 게시글 하나만 가져옴
    article = Article.objects.get(pk=pk)
	# POST 요청 처리
    if request.method == 'POST':
        # POST : input 값 가져와서, 검증하고, DB에 저장
        article_form = ArticleForm(request.POST, instance=article)
        # 유효성 검사를 통과하면
        if article_form.is_valid():
            # DB에 저장
            article_form.save()
            # detail 페이지로 redirect
            return redirect('articles:detail', article.pk)
    # GET 요청 처리
    else:
        # 특정 게시글의 데이터를 form에 입력
        article_form = ArticleForm(instance=article)
    # template에 전달
    context = {
        'article_form': article_form
    }
	# 게시글 수정 페이지로 이동
    return render(request, 'articles/update.html', context)
```



### 5. Admin site

> 사용자가 아닌 서버 관리자가 활용하기 위한 페이지로, 모델 클래스를 admin.py에 등록하고 관리

#### 5-1. admin 계정 생성

```bash
# admin 계정 생성
$ python manage.py createsuperuser

# Username 설정
Username: admin 

# Email 설정
Email address: (선택사항 - 생략) 

# Password 설정 및 재확인
Password: (입력해도 보안상 보이지 않음)
Password (again): (입력해도 보안상 보이지 않음)
```

#### 5-2. admin site 접속 후 로그인

- http://127.0.0.1:8000/admin/ 로 접속 후 로그인

#### 5-3. Model 클래스 등록

- `articles/admin.py` 파일에 임포트 추가 및 클래스 추가

```python
from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    fields = ['title']

admin.site.register(Article, ArticleAdmin)
```



### 6. Static files

> 웹 서버는 요청 받은 URL로 서버에 존재하는 정적 자원(static resource)를 제공
>
> 예를 들어 이미지, 자바 스크립트, CSS와 같은 미리 준비된 추가 파일을 제공
>
> 정적 파일 : 응답할 때 별도의 처리 없이 요청한 파일 내용을 그대로 보여주는 파일

#### 6-0. STATIC files 설정

- `django.contrib.staticfiles`가 `pjt/settings.py` 파일의 `INSTALLED_APPS`에 포함되어 있는지 확인

```python
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',
]
```

- `pjt/settings.py` 파일의 `INSTALLED_APPS`에 `STATIC_URL` 설정

```python
STATIC_URL = '/static/'
```

- 기본 경로를 제외하고 추가적인 정적 파일 경로 목록 정의 : `STATICFILES_DIRS`

#### 6-1. 정적 파일 저장

- `articles/static/articles` 폴더 생성 후, 정적 파일 폴더별 관리
- `articles/images` 폴더 생성 후, 이미지 정적 파일 관리
- `articles/css` 폴더 생성 후, CSS 정적 파일 관리

#### 6-2. Template 설정

- 사용자 정의 템플릿 태그 세트를 로드(load)

```html
{% load static %}
```

- 정적 파일 활용 예시

```html
img src="{% static 'articles/images/pixar.png' %}" alt="pixar image">
```



### 7. Django-Bootstrap 5

