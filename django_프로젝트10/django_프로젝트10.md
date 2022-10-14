# Django 프로젝트 10



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

#### 1-3. Django, 추가 패키지 설치 및 기록

> 가상환경 실행한 상태에서 패키지 설치

```bash
# Django LTS 버전 설치
$ pip install django==3.2.13

# Django-Bootstrap5 패키지 설치
$ pip install django-bootstrap5

# Django-Extensions 패키지 설치
$ pip install django-extensions

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
      <a class="red click" href="">Login</a>
      <a class="yellow click" href="">Signup</a>
      <a class="green click" href="">Member</a>
      <a class="blue click" href="">Home</a>
    </div>
  </div>
{% endblock %}
```



### 4. account App

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



### 6. 회원관리 기능 구현

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
        Signup
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
<a class="yellow" href="{% url 'accounts:signup' %}">Signup</a>
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
        Login
      </h1>
    </div>
    <div class="card-body box">
      <form action="" method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <div class="left">
          <input class="btn red click" type="submit" value="OK">
        </div>
      </form>
    </div>
  </div>
{% endblock %}
```

##### (4)  페이지 연결

- `config/templates/index.html` 파일에 추가

```html
<a class="red" href="{% url 'accounts:login' %}">Login</a>
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
  <div class="box w-50">
    <h1 class="text-center">
      <i class="bi bi-people"></i>
      Member
    </h1>
    <div class="card-footer left my-2">
    {% if request.user.is_authenticated %}
      <a class="red click" href="">Logout</a>
      <a class="yellow click" href="">Home</a>
    {% else %}
      <a class="red click" href="">Login</a>
      <a class="yellow click" href="{% url 'accounts:signup' %}">Signup</a>
      <a class="green click" href="">Home</a>
    {% endif %}
    </div>
    <table class="table align-middle text-center table-borderless">
      <thead class="bg-dark text-light">
        <tr>
          <th scope="col">no</th>
          <th scope="col">username</th>
          <th scope="col">date_joined</th>
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

##### (3)  페이지 연결

- `config/templates/index.html` 파일에 추가

```html
<a class="green click" href="{% url 'accounts:index' %}">Member</a>
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
  <div class="card shadow w-50">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-person-badge"></i>
        {{ user }}
        Profile
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
        <a class="red click" href="">Logout</a>
        <a class="yellow click" href="">Update</a>
        <a class="green click" href="{% url 'accounts:index' %}">Member</a>
        <a class="blue click" href="">Home</a>
      {% else %}
        <a class="red click" href="{% url 'accounts:index' %}">Member</a>
        <a class="yellow click" href="">Home</a>
      {% endif %}
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
<a class="red click" href="{% url 'accounts:logout' %}">Logout</a>
```



### 7. reviews App

#### 7-1. App 생성

```bash
# Django 앱 생성
python manage.py startapp reviews
```

#### 7-2. App 등록

- `config/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'reviews',
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
    path('reviews/', include('reviews.urls')),
]
```

- `reviews/urls.py` 파일 생성

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
]

```

#### 7-4. View 설정

- `reviews/views.py` 파일에 함수 생성

```python
from django.shortcuts import render

def index(request):

    return render(request, 'reviews/index.html')
```

#### 7-5. Templates 관리

- `reviews/templates/reviews` 폴더 생성 후, 템플릿 관리
- `reviews/index.html` 파일 생성



### 8. Review Model 정의

#### 8-1. 클래스 정의

- `reviews/models.py` 파일에 클래스 추가

```python
from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    movie_name = models.CharField(max_length=20)
    grade_choices = (
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    )
    grade = models.IntegerField(choices=grade_choices)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```

#### 8-2. 마이그레이션 파일 생성

- `reviews/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

#### 8-3. DB 반영

```bash
$ python manage.py migrate
```



### 9. 리뷰관리 기능 구현

#### 9-1. 리뷰 작성 기능

##### (1) ModelForm 선언

- `reviews/forms.py` 파일 생성

```python
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'movie_name', 'grade']
```

##### (2) URL 설정

- `reviews/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
]
```

##### (3) View 설정

- `reviews/views.py` 파일에 임포트 추가 및 함수 생성

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm

...

@login_required
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:index')
    else:
        form = ReviewForm()
    context = {
        'form': form
    }
    return render(request, 'reviews/create.html', context=context)
```

##### (4) html 작성

- `reviews/create.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="card shadow w-50">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-pencil-fill"></i>
        Review
      </h1>
    </div>
    <div class="card-body box">
      <form action="" method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <div class="left">
          <input class="btn red click" type="submit" value="OK">
        </div>
      </form>
    </div>
  </div>
{% endblock %}
```

#### 9-2. 리뷰 목록 기능

##### (1) View 설정

- `reviews/views.py` 파일에 임포트 추가 및 함수 수정

```python
...
from .models import Review

...

def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/index.html', context)
```

##### (2) html 작성

- `reviews/index.html` 파일 수정

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="box w-100 m-3 p-5">
    <h1 class="text-center">
      <i class="bi bi-card-list"></i>
      Review List
    </h1>
    <div class="card-footer left my-2">
      {% if request.user.is_authenticated %}
        <a class="red click" href="{% url 'accounts:logout' %}">Logout</a>
        <a class="yellow click" href="{% url 'reviews:create' %}">Write</a>
      {% else %}
        <a class="red click" href="{% url 'accounts:login' %}">Login</a>
        <a class="yellow click" href="{% url 'accounts:signup' %}">Signup</a>
      {% endif %}
    </div>
    <table class="table align-middle text-center table-borderless">
      <thead class="bg-dark text-light">
        <tr>
          <th scope="col">no</th>
          <th scope="col">title</th>
          <th scope="col">movie</th>
          <th scope="col">grade</th>
        </tr>
      </thead>
      <tbody class="bg-light">
        {% for review in reviews %}
          <tr>
            <td>{{ review.pk }}</td>
            <td>
              <a class="text-dark" href="">{{ review.title }}</a>
            </td>
            <td>{{ review.movie_name }}</td>
            <td>{{ review.get_grade_display }}</td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
{% endblock %}
```

##### (3) 페이지 연결

- `config/templates/index.html` 파일에 추가

```html
<a class="blue click" href="{% url 'reviews:index' %}">Home</a>
```

- `accounts/index.html` 파일에 추가

```html
<a class="yellow click" href="{% url 'reviews:index' %}">Home</a>
```

- `accounts/detail.html` 파일에 추가

```html
<a class="blue click" href="{% url 'reviews:index' %}">Home</a>
```

- `accounts/views.py` 파일 수정

```python
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('reviews:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('reviews:index')
```

#### 9-3. 리뷰 상세보기 기능

##### (1) URL 설정

- `reviews/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
]
```

##### (2) View 설정

- `reviews/views.py` 파일에 함수 생성

```python
...

def detail(request, pk):
    review = Review.objects.get(pk=pk)
    context = {
        'review': review
    }
    return render(request, 'reviews/detail.html', context)
```

##### (3) html 작성

- `reviews/detail.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="card shadow w-50">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-card-list"></i>
        {{ review.title }}
      </h1>
    </div>
    <div class="card-body box">
      <dl class="row">
        <dt class="col-sm-3 text-center">movie</dt>
        <dd class="col-sm-9">{{ review.title }}</dd>
        <dt class="col-sm-3 text-center">grade</dt>
        <dd class="col-sm-9">
          {{ review.get_grade_display }}
          {{ review.grade }}
        </dd>
        <dt class="col-sm-3 text-center">review</dt>
        <dd class="col-sm-9">{{ review.content }}</dd>
        <dt class="col-sm-3 text-center">created_at</dt>
        <dd class="col-sm-9">{{ review.created_at | date:"Y-m-d" }}</dd>
        <dt class="col-sm-3 text-center">updated_at</dt>
        <dd class="col-sm-9">{{ review.updated_at | date:"Y-m-d" }}</dd>
      </dl>
    </div>
    <div class="card-footer left">
      {% if request.user.is_authenticated %}
        <a class="red click" href="">Edit</a>
        <a class="yellow click" href="">Delete</a>
        <a class="green click" href="{% url 'reviews:index' %}">Home</a>
      {% else %}
        <a class="red click" href="{% url 'reviews:index' %}">Home</a>
      {% endif %}
    </div>
  </div>
{% endblock %}
```

##### (4) 페이지 연결

- `reviews/index.html` 파일에 추가

```html
<a class="text-dark" href="{% url 'reviews:detail' review.pk %}">{{ review.title }}</a>
```

#### 9-4. 리뷰 수정 기능

##### (1) URL 설정

- `reviews/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
]
```

##### (2) View 설정

- `reviews/views.py` 파일에 함수 생성

```python
...

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:detail', review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form
    }
    return render(request, 'reviews/update.html', context=context)
```

##### (3) html 작성

- `reviews/update.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="card shadow w-50">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-pencil-fill"></i>
        Review Edit
      </h1>
    </div>
    <div class="card-body box">
      <form action="" method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <div class="left">
          <input class="btn red click" type="submit" value="OK">
        </div>
      </form>
    </div>
  </div>
{% endblock %}
```

##### (4) 페이지 연결

- `reviews/detail.html` 파일에 추가

```html
<a class="red click" href="{% url 'reviews:update' %}">Edit</a>
```

#### 9-5. 리뷰 삭제 기능

##### (1) URL 설정

- `reviews/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
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
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect('reviews:index')
```

##### (3) 페이지 연결

- `reviews/detail.html` 파일에 추가

```html
<a class="yellow click" href="{% url 'reviews:delete' review.pk %}">Delete</a>
```



### 10. Header & Footer

#### 10-1. Header

- `config/templates/header.html` 파일 생성

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
  <div class="container-fluid">
    <a class="navbar-brand">
      <i class="bi bi-brightness-high"></i>
    </a>
    {% if request.user.is_authenticated %}
      <a class="text-white m-0" href="{% url 'accounts:detail' user.pk %}">
        Hello
        {{ user }}
      </a>
    {% endif %}
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        {% if request.user.is_authenticated %}
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="{% url 'accounts:logout' %}">Logout</a>
          </li>
        {% else %}
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="{% url 'accounts:login' %}">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:signup' %}">Signup</a>
          </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
```

#### 10-2. Footer

- `config/templates/footer.html` 파일 생성

```html
<footer class="m-0 p-3 bg-dark fixed-bottom">
  <div class="container-fluid">
    <p class="m-0 text-center text-light">© 2022 C.M.A</p>
  </div>
</footer>
```

#### 10-3. 활용

- 필요한 페이지마다 추가

```html
{% include 'header.html' %}
{% include 'footer.html' %}
```
