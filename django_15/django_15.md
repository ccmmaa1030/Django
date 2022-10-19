# Django 14



### 1. 환경 설정

#### 1-1. 가상환경 생성 및 실행

> 가상환경 : 프로젝트별 별도 패키지 관리

```bash
# 가상환경 생성
$ python -m venv venv

# 가상환경 폴더 생성 확인
$ ls

# 가상환경 실행
$ source venv/Scripts/activate
(venv)
```

#### 1-2. .gitignore

> https://www.toptal.com/developers/gitignore/

```bash
$ touch .gitignore
```

#### 1-3. Django, 추가 라이브러리 설치 및 기록

> 가상환경 실행한 상태에서 라이브러리 설치

```bash
# Django LTS 버전 설치
$ pip install django==3.2.13

# Django-Bootstrap5 설치
$ pip install django-bootstrap5

# Django-Extensions 설치
$ pip install django-extensions

# Pillow 설치
$ pip install Pillow

# PILkit(Pillow 헬퍼) 설치
$ pip install pilkit

# django-imagekit(썸네일 헬퍼 장고 앱) 설치
$ pip install django-imagekit

# 패키지 설치 확인
$ pip list

# 패키지 기록
$ pip freeze > requirements.txt
```

#### 1-4. Django 프로젝트 생성

```bash
# Django 프로젝트 생성
$ django-admin startproject config .

# 프로젝트 폴더 생성 확인
$ ls
```

#### 1.5 패키지 등록

- `config/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'django_bootstrap5',
    'django_extensions',
    'imagekit'
    ...
]
```

#### 1-6. 기타

```bash
# 서버 정상 실행 확인
$ python manage.py runserver
# ctrl + c 눌러서 종료

# VS code 실행
$ code .
```



### 2. Template 및 Static Files 관리

#### 2-1 Templates 설정

- `config/templates` 폴더 생성 후, 템플릿 관리
- `config/settings.py` 파일의 `TEMLATES`의 `DIRS` 추가

```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'config' / 'templates'],
        ...
    },
]
```

#### 2-2. STATIC files 설정

- `django.contrib.staticfiles`가 `config/settings.py` 파일의 `INSTALLED_APPS`에 포함되어 있는지 확인

```python
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',
]
```

- `config/settings.py` 파일의 `INSTALLED_APPS`에 `STATIC_URL` 설정

```python
STATIC_URL = '/static/'
```

- `config/static/` 폴더 생성 후, 정적 파일 폴더별 관리
- 기본 경로를 제외하고 추가적인 정적 파일 경로 목록 정의 : `STATICFILES_DIRS`

```python
import os

...

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "config", "static")]
```

- `static/css` 폴더 생성 후, css 파일 관리

#### 2-3. 기본 Templates 관리

- `templates/base.html` 파일 생성

```bash
{% load django_bootstrap5 %}
{% load static %}

<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% bootstrap_css %}
    {% bootstrap_javascript %}
    {% bootstrap_messages %}
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <title>Document</title>
  </head>

  <body>
    {% block content %}{% endblock %}
  </body>

</html>
```



### 3. 시작 페이지

#### 3-1. URL 설정

- `config/urls.py` 파일에 추가

```python
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
]
```

#### 3-2. View 설정

- `config/views.py` 파일 생성

```python
from django.shortcuts import render

def index(request):

    return render(request, 'index.html')
```

#### 3-3. html 작성

- `config/templates/index.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="card shadow">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-brightness-high"></i>
        Welcome
      </h1>
    </div>
    <div class="card-body box">
      <a class="red click" href="">메인 페이지</a>
      <a class="yellow click" href="">회원가입</a>
      <a class="green click" href="">로그인</a>
      <a class="blue click" href="">글 작성하기</a>
    </div>
  </div>
{% endblock %}
```



### 4. accounts App

#### 4-1. App 생성

```bash
# Django 앱 생성
python manage.py startapp accounts
```

#### 4-2. App 등록

- `config/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'accounts',
    ...
]
```

#### 4-3. URL 설정

> app 단위의 URL 관리

- `config/urls.py` 파일에 추가

```python
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('accounts.urls')),
]
```

- `accounts/urls.py` 파일 생성

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
]

```

#### 4-4. View 설정

- `accounts/views.py` 파일에 함수 생성

```python
from django.shortcuts import render

def index(request):

    return render(request, 'accounts/index.html')
```

#### 4-5. Templates 관리

- `accounts/templates/accounts` 폴더 생성 후, 템플릿 관리
- `accounts/index.html` 파일 생성



### 5. User Model 정의

> Django AbstractUser 모델 상속

#### 5-1. 클래스 정의

- `accounts/models.py` 파일에 클래스 추가

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```

#### 5-2. User Model 등록

- `config/settings.py` 파일에  `AUTH_USER_MODEL` 추가

```python
# User Model
AUTH_USER_MODEL = 'accounts.User'
```

#### 5-3. 마이그레이션 파일 생성

- `accounts/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

#### 5-4. DB 반영

```bash
$ python manage.py migrate
```



### 6. 회원 CRUD 기능 구현

#### 6-1. 회원가입 기능

##### (1) CustomUserCreationForm 생성

- `accounts/forms.py` 파일 생성

```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2',)
```

##### (2) URL 설정

- `accounts/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',  views.signup, name='signup'),
]
```

##### (3) View 설정

- `accounts/views.py` 파일에 임포트 추가 및 함수 생성

```python
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

...

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/signup.html', context)
```

##### (4) html 작성

- `accounts/signup.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="card shadow w-50">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-check-square"></i>
        회원가입
      </h1>
    </div>
    <div class="card-body box">
      <form action="" method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <div class="left">
          <input class="btn yellow click" type="submit" value="OK">
        </div>
      </form>
    </div>
  </div>
{% endblock %}
```

##### (4)  페이지 연결

- `config/templates/index.html` 파일에 추가

```html
<a class="yellow click" href="{% url 'accounts:signup' %}">회원가입</a>
```

#### 6-2. 로그인 기능

##### (1) URL 설정

- `accounts/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',  views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
```

##### (2) View 설정

- `accounts/views.py` 파일에 임포트 추가 및 함수 생성

```python
...
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

...

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
```

##### (3) html 작성

- `accounts/login.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="card shadow w-50">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-box-arrow-in-left"></i>
        로그인
      </h1>
    </div>
    <div class="card-body box">
      <form action="" method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <div class="left">
          <input class="btn green click" type="submit" value="OK">
        </div>
      </form>
    </div>
  </div>
{% endblock %}
```

##### (4)  페이지 연결

- `config/templates/index.html` 파일에 추가

```html
<a class="green click" href="{% url 'accounts:login' %}">로그인</a>
```

#### 6-3. 회원 목록 기능

##### (1) View 설정

- `accounts/views.py` 파일에 임포트 추가 및 함수 수정

```python
...
from django.contrib.auth import get_user_model

def index(request):
    users = get_user_model().objects.all()
    context = {
        'users': users
    }
    return render(request, 'accounts/index.html', context)
```

##### (2) html 작성

- `accounts/index.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="box w-100 m-3 p-5">
    <h1 class="text-center">
      <i class="bi bi-people"></i>
      회원목록
    </h1>
    <div class="left my-2">
      {% if request.user.is_authenticated %}
        <a class="btn red click" href="">로그아웃</a>
      {% else %}
        <a class="yellow click" href="{% url 'accounts:signup' %}">회원가입</a>
        <a class="green click" href="">로그인</a>
      {% endif %}
    </div>
    <table class="table align-middle text-center table-borderless">
      <thead class="bg-dark text-light">
        <tr>
          <th scope="col">번호</th>
          <th scope="col">유저</th>
          <th scope="col">가입일</th>
        </tr>
      </thead>
      <tbody class="bg-light">
        {% for user in users %}
          <tr>
            <td>{{ user.pk }}</td>
            <td>
              <a class="text-dark" href="">{{ user.username }}</a>
            </td>
            <td>{{ user.date_joined }}</td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
{% endblock %}
```

#### 6-4. 회원 상세정보 기능

##### (1) URL 설정

- `accounts/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('<int:pk>/', views.detail, name='detail'),
]
```

##### (2) View 설정

- `accounts/views.py` 파일에 임포트 추가 및 함수 생성

```python
...

def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        'user': user
    }
    return render(request, 'accounts/detail.html', context)
```

##### (3) html 작성

- `accounts/detail.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="d-flex flex-column align-items-center mt-5 pt-5">
    <div class="card shadow w-75">
      <div class="card-header bg-dark">
        <h1 class="text-light">
          <i class="bi bi-person-badge"></i>
          {{ user }}의 프로필
        </h1>
      </div>
      <div class="card-body box">
        <dl class="row">
          <dt class="col-sm-3 text-center">username</dt>
          <dd class="col-sm-9">{{ user.username }}</dd>
          <dt class="col-sm-3 text-center">date_joined</dt>
          <dd class="col-sm-9">{{ user.date_joined }}</dd>
          <dt class="col-sm-3 text-center">email</dt>
          <dd class="col-sm-9">{{ user.email }}</dd>
          <dt class="col-sm-3 text-center">last_name</dt>
          <dd class="col-sm-9">{{ user.last_name }}</dd>
          <dt class="col-sm-3 text-center">first_name</dt>
          <dd class="col-sm-9">{{ user.first_name }}</dd>
        </dl>
      </div>
      <div class="card-footer left">
        {% if request.user.is_authenticated %}
          <a class="btn red click" href="">로그아웃</a>
          <a class="btn yellow click" href="">정보 수정</a>
          <a class="btn green click" href="{% url 'accounts:index' %}">회원목록</a>
          <a class="btn blue click" href="">메인 페이지</a>
        {% else %}
          <a class="btn green click" href="{% url 'accounts:index' %}">회원목록</a>
          <a class="btn blue click" href="">메인 페이지</a>
        {% endif %}
      </div>
    </div>
  </div>
{% endblock %}
```

##### (3)  페이지 연결

- `accounts/index.html` 파일에 추가

```html
<a class="text-dark" href="{% url 'accounts:detail' user.pk %}">{{ user.username }}</a>
```

#### 6-5. 회원 정보수정 기능

##### (1) CustomUserCreationForm 생성

- `accounts/forms.py` 파일에 추가

```python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

...

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email',)
```

##### (2) URL 설정

- `accounts/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('<int:pk>/', views.detail, name='detail'),
    path('update/', views.update, name='update'),
]
```

##### (3) View 설정

- `accounts/views.py` 파일에 임포트 추가 및 함수 생성

```python
...
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required

...

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)
```

##### (4) html 작성

- `accounts/update.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="card shadow w-50">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-check-square"></i>
        Update
      </h1>
    </div>
    <div class="card-body box">
      <form action="" method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <div class="left">
          <input class="btn yellow click" type="submit" value="OK">
        </div>
      </form>
    </div>
  </div>
{% endblock %}
```

##### (5)  페이지 연결

- `accounts/detail.html` 파일에 추가

```html
<a class="yellow click" href="{% url 'accounts:update' %}">Update</a>
```

#### 6-6. 로그아웃 기능

##### (1) URL 설정

- `accounts/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('<int:pk>/', views.detail, name='detail'),
    path('update/', views.update, name='update'),
    path('logout/', views.logout, name='logout'),
]
```

##### (2) View 설정

- `accounts/views.py` 파일에 임포트 추가 및 함수 생성

```python
...
from django.contrib.auth import logout as auth_logout

...

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')
```

##### (3)  페이지 연결

- `accounts/detail.html` 파일에 추가

```html
<a class="btn red click" href="{% url 'accounts:logout' %}">로그아웃</a>
```



### 7. articles App

#### 7-1. App 생성

```bash
# Django 앱 생성
python manage.py startapp articles
```

#### 7-2. App 등록

- `config/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'articles',
    ...
]
```

#### 7-3. URL 설정

> app 단위의 URL 관리

- `config/urls.py` 파일에 추가

```python
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
]
```

- `articles/urls.py` 파일 생성

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
]
```

#### 7-4. View 설정

- `articles/views.py` 파일에 함수 생성

```python
from django.shortcuts import render

def index(request):

    return render(request, 'articles/index.html')
```

#### 7-5. Templates 관리

- `articles/templates/articles` 폴더 생성 후, 템플릿 관리
- `articles/index.html` 파일 생성



### 8. Article Model 정의

#### 8-1. 클래스 정의

- `articles/models.py` 파일에 클래스 추가

```python
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    thumbnail = ProcessedImageField(upload_to='images/', blank=True,
                                    processors=[ResizeToFill(400, 300)],
                                    format='JPEDG',
                                    options={'quality': 80}
                                    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```

#### 8-2. 마이그레이션 파일 생성

- `articles/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

#### 8-3. DB 반영

```bash
$ python manage.py migrate
```



### 9. 게시글 CRUD 기능 구현

#### 9-1. 게시글 작성 기능

##### (1) ModelForm 선언

- `articles/forms.py` 파일 생성

```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Aritlce
        fields = ['title', 'content', 'image']
```

##### (2) Media 설정

- `config/settings.py` 파일에 `MEDIA_ROOT`, `MEDIA_URL` 설정

```python
MEDIA_ROOT = BASE_DIR / 'images'
MEDIA_URL = '/media/'
```

- `config/urls.py` 파일에 업로드 한 미디어 파일 제공

```python
...
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

##### (3) URL 설정

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
]
```

##### (4) View 설정

- `articles/views.py` 파일에 임포트 추가 및 함수 생성

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm

...

@login_required
def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context=context)
```

##### (5) html 작성

- `articles/form.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="card shadow w-50">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-pencil-fill"></i>
        {% if request.resolver_match.url_name == 'create' %}
          글 작성
        {% else %}
          글 수정
        {% endif %}
      </h1>
    </div>
    <div class="card-body box">
      <form action="" method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {% bootstrap_form article_form %}
        <div class="left">
          <input class="btn red click" type="submit" value="OK">
        </div>
      </form>
    </div>
  </div>
{% endblock %}
```

##### (3) 페이지 연결

- `config/templates/index.html` 파일에 추가

```html
<a class="blue click" href="{% url 'articles:create' %}">글 작성하기</a>
```

#### 9-2. 게시글 목록 기능

##### (1) View 설정

- `articles/views.py` 파일에 임포트 추가 및 함수 수정

```python
...
from models import Article

def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)
```

##### (2) html 작성

- `articles/index.html` 파일 수정

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="box w-100 m-3 p-5">
    <h1 class="text-center">
      <i class="bi bi-card-list"></i>
      게시판
    </h1>
    <div class="left my-2">
      {% if request.user.is_authenticated %}
        <a class="btn red click" href="{% url 'accounts:logout' %}">로그아웃</a>
        <a class="btn blue click" href="{% url 'articles:create' %}">글 작성</a>
      {% else %}
        <a class="btn yellow click" href="{% url 'accounts:signup' %}">회원가입</a>
        <a class="btn green click" href="{% url 'accounts:login' %}">로그인</a>
      {% endif %}
    </div>
    <div class="row">
      {% for article in articles %}
        <div class="col-4">
          <div class="card">
            <img src="{{ article.image.url }}" class="card-img-top" alt="thumbnail">
            <div class="card-body">
              <a class="text-dark fs-4 fw-bold mx-0" href="">
                {{ article.pk }}번 :
                {{ article.title }}
              </a>
              <p class="m-0 w-100 text-end">
                {{ article.created_at | date:"Y-m-d" }}
              </p>
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
{% endblock %}
```

##### (3) 페이지 연결

- `config/templates/index.html` 파일에 추가

```html
<a class="red click" href="{% url 'articles:index' %}">메인 페이지</a>
```

- `accounts/detail.html` 파일에 추가

```html
<a class="btn blue click" href="{% url 'articles:index' %}">메인 페이지</a>
```

#### 9-3. 게시글 상세보기 기능

##### (1) URL 설정

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
]
```

##### (2) View 설정

- `articles/views.py` 파일에 함수 생성

```python
...

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)
```

##### (3) html 작성

- `articles/detail.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="d-flex flex-column align-items-center mt-5 pt-5">
    <div class="card shadow w-75">
      <div class="card-header bg-dark">
        <h1 class="text-light">
          <i class="bi bi-card-list"></i>
          {{ article.pk }}번 게시글
        </h1>
      </div>
      <div class="card-body box">
        <dl class="row">
          <img class="mb-4" src="{{ article.image.url }}" alt="{{ article.image }}">
          <dt class=" col-sm-3 text-center">제목</dt>
          <dd class="col-sm-9">{{ article.title }}</dd>
          <dt class="col-sm-3 text-center">내용</dt>
          <dd class="col-sm-9">{{ article.content }}</dd>
          <dt class="col-sm-3 text-center">작성일</dt>
          <dd class="col-sm-9">{{ article.created_at | date:"Y-m-d" }}</dd>
          <dt class="col-sm-3 text-center">수정일</dt>
          <dd class="col-sm-9">{{ article.updated_at | date:"Y-m-d" }}</dd>
        </dl>
      </div>
      <div class="card-footer left">
        {% if request.user.is_authenticated %}
          <a class="btn blue click mx-2" href="">글 수정</a>
          <a class="btn red click" href="">글 삭제</a>
        {% endif %}
      </div>
    </div>
  </div>
{% endblock %}
```

##### (4) 페이지 연결

- `articles/index.html` 파일에 추가

```html
<a class="text-dark fs-4 fw-bold mx-0" href="{% url 'articles:detail' article.pk %}">
    {{ article.pk }}번 :
    {{ article.title }}
</a>
```

#### 9-4. 게시글 수정 기능

##### (1) URL 설정

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
]
```

##### (2) View 설정

- `articles/views.py` 파일에 함수 생성

```python
...

@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```

##### (3) 페이지 연결

- `articles/detail.html` 파일에 추가

```html
<a class="btn blue click mx-2" href="{% url 'articles:update' article.pk %}">글 수정</a>
```

#### 9-5. 게시글 삭제 기능

##### (1) URL 설정

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
```

##### (2) View 설정

- `reviews/views.py` 파일에 함수 생성

```python
...

@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')
```

##### (3) 페이지 연결

- `reviews/detail.html` 파일에 추가

```html
<a class="btn red click" href="{% url 'articles:delete' article.pk %}">글 삭제</a>
```



### 10. Comment Model 정의

#### 10-1. 클래스 정의

- `articles/models.py` 파일에 클래스 추가

```python
...

class Comment(models.Model):
    content = models.TextField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
```

#### 10-2. 마이그레이션 파일 생성

- `articles/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

#### 10-3. DB 반영

```bash
$ python manage.py migrate
```



### 11. 댓글 CRUD 기능 구현

#### 11-1. 댓글 작성 기능

##### (1) ModelForm 선언

- `articles/forms.py` 파일에 추가

```python
from django import forms
from .models import Article, Comment

...

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
```

##### (2) URL 설정

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comments/', views.comment_create, name='comment_create'),
]
```

##### (3) View 설정

- `articles/views.py` 파일에 함수 수정

```python
...
from .forms import ArticleForm, CommentForm

...

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        'article': article,
        'comment_form': comment_form
    }
    return render(request, 'articles/detail.html', context)
```

- `articles/views.py` 파일에 함수 생성

```python
...

def comment_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.save()
    return redirect('articles:detail', article.pk)
```

##### (4) html 작성

- `articles/detail.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="d-flex flex-column align-items-center">
    
      ...
      
    <hr>
    <form class="w-75" action="{% url 'articles:comment_create' article.pk %}" method="POST">
      {% csrf_token %}
      {% bootstrap_form comment_form %}
      <div class="left">
        <input class="btn green click" type="submit" value="OK">
      </div>
    </form>
  </div>
{% endblock %}
```

#### 11-2. 댓글 목록 기능

##### (1) View 설정

- `articles/views.py` 파일에 임포트 추가 및 함수 수정

```python
...

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)
```

##### (2) html 작성

- `articles/index.html` 파일 수정

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="d-flex flex-column align-items-center">
    
     ...
      
    <hr>
    {% for comment in comments %}
      <div class="card w-75 my-1">
        <div class="card-body row">
          <div class="col-10">
            <p class="my-2">{{ comment.content }}</p>
          </div>
          <div class="col-2">
            <a class="btn yellow click" href="">댓글 삭제</a>
          </div>
        </div>
      </div>
      {% empty %}
      <p>댓글 없음</p>
    {% endfor %}
  </div>
{% endblock %}
```

#### 11-3. 댓글 삭제 기능

##### (1) URL 설정

- `articles/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
]
```

##### (2) View 설정

- `reviews/views.py` 파일에 함수 생성

```python
...

def comment_delete(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', pk)
```

##### (3) 페이지 연결

- `reviews/detail.html` 파일에 추가

```html
<a class="btn yellow click" href="{% url 'articles:comment_delete' article.pk comment.pk %}">댓글 삭제</a>
```



### 12. 회원 + 게시글 + 댓글 기능

#### 12-0. Model 재정의

##### (1) 클래스 재정의

- `articles/models.py` 파일에 클래스 추가

```python
...
from django.conf import settings

class Article(models.Model):
    ...
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   
class Comment(models.Model):
    ...
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

#### 8-2. 마이그레이션 파일 생성

- `articles/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

#### 8-3. DB 반영

```bash
$ python manage.py migrate
```

#### 12-1. 회원 + 게시글 기능

##### (1) View 설정

- `articles/views.py` 파일의 함수 수정

```python
...
from django.contrib import messages

@login_required
def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            # article_form.save() -> 아래 코드로 수정
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context=context)

@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    # 작성자가 맞는지 확인
    if request.user == article.user: 
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, request.FILES, instance=article)
            if article_form.is_valid():
                article_form.save()
                return redirect('articles:detail', article.pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    # 아닐 경우 메세지 띄움
    else:
        messages.warning(request, '작성자만 수정할 수 있습니다.')
        return redirect('articles:detail', article.pk)
```

##### (2) html 작성

- `articles/index.html` 파일에 추가

```html
<a href="{% url 'accounts:detail' article.user.pk %}">
   {{ article.user.username }
</a>
```

- `articles/detail.html` 파일에 추가

```html
<dt class=" col-sm-3 text-center">작성자</dt>
    <dd class="col-sm-9">
        <a class="text-black" href="{% url 'accounts:detail' article.user.pk %}">
          {{ article.user.username }}
        </a>
    </dd>

...

<div class="card-footer left">
    {% if request.user.is_authenticated %}
        {% if request.user == article.user %}
            <a class="btn blue click mx-2" href="{% url 'articles:update' article.pk %}">글 수정</a>
            <a class="btn red click" href="{% url 'articles:delete' article.pk %}">글 삭제</a>
        {% endif %}
    {% endif %}
</div>
```

- `accounts/detail.html` 파일에 추가

```html
<div>
    <p class="text-muted text-center">{{ user.article_set.count }}개의 게시글을 작성하였습니다.</p>
    {% for article in user.article_set.all %}
        <div class="card w-100 my-1">
            <div class="card-body row p-1 w-100">
                <div class="col-2 py-1">
                    <p class="my-1 mx-3">{{ forloop.counter }}</p>
                </div>
                <div class="col-10 py-1">
                    <a class="text-dark" href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
                </div>
            </div>
        </div>
    {% endfor %}
</div>
```

#### 12-2. 회원 + 댓글 기능

##### (1) View 설정

- `articles/views.py` 파일의 함수 수정

```python
# 로그인이 필요한 기능
@login_required
def comment_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        # 댓글 작성자는 현재 로그인 한 유저
        comment.user = request.user
        comment.save()
    return redirect('articles:detail', article.pk)
```

##### (2) html 작성

- `articles/detail.html` 파일에 추가

```html
...

{% for comment in comments %}
  <p>{{ comments|length }}개의 댓글이 있습니다.</p>
  <div class="card w-75 my-1">
    <div class="card-body row p-1">
      <div class="col-2 py-1">
        <p class="my-1 mx-3">{{ comment.user.username }}</p>
      </div>
      <div class="col-8 py-1">
        <p class="my-1 mx-3">{{ comment.content }}</p>
      </div>
      <div class="col-2 py-1">
        <a class="btn btn-sm red click" href="{% url 'articles:comment_delete' article.pk comment.pk %}">댓글 삭제</a>
      </div>
    </div>
  </div>
  {% empty %}
  <p>댓글이 없습니다.</p>
{% endfor %}
```

- `accounts/detail.html` 파일에 추가

```html
<div>
    <p class="text-muted text-center">{{ user.comment_set.count }}개의 댓글을 작성하였습니다.</p>
    {% for comment in user.comment_set.all %}
        <div class="card w-100 my-1">
            <div class="card-body row p-1 w-100">
                <div class="col-2 py-1">
                    <p class="my-1 mx-3">{{ forloop.counter }}</p>
                </div>
                <div class="col-10 py-1">
                    <a class="text-dark" href="{% url 'articles:detail' comment.pk %}">{{ comment.content }}</a>
                </div>
            </div>
        </div>
    {% endfor %}
</div>
```



### 13. Header & Footer

#### 13-1. Header

- `config/templates/header.html` 파일 생성

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
  <div class="container-fluid">
    <a class="navbar-brand">
      <i class="bi bi-brightness-high"></i>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="{% url 'articles:index' %}">메인 페이지</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{% url 'accounts:index' %}">회원목록</a>
        </li>
        {% if request.user.is_authenticated %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:detail' user.pk %}">회원정보</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:logout' %}">로그아웃</a>
          </li>
        {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'articles:singup' %}">회원가입</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:login' %}">로그인</a>
          </li>
        {% endif %}
        <li class="nav-item">
          <a class="nav-link" href="{% url 'articles:create' %}">글 작성하기</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

#### 13-2. Footer

- `config/templates/footer.html` 파일 생성

```html
<footer class="m-0 p-3 bg-dark fixed-bottom">
  <div class="container-fluid">
    <p class="m-0 text-center text-light">© 2022 C.M.A</p>
  </div>
</footer>
```

#### 13-3. 활용

- 필요한 페이지마다 추가

```html
{% include 'header.html' %}
{% include 'footer.html' %}
```

