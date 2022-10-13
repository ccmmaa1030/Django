# Django 12



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

#### 1-2. Django, 추가 패키지 설치 및 기록

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

#### 1-3. Django 프로젝트 생성

```bash
# Django 프로젝트 생성
$ django-admin startproject pjt .

# 프로젝트 폴더 생성 확인
$ ls
```

#### 1.4 패키지 등록

- `pjt/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'django_bootstrap5',
    'django_extensions',
    ...
]
```

#### 1-5. 기타

```bash
# 서버 정상 실행 확인
$ python manage.py runserver
# ctrl + c 눌러서 종료

# VS code 실행
$ code .
```



### 2. Template 및 Static Files 관리

#### 2-1 Templates 설정

- `pjt/templates` 폴더 생성 후, 템플릿 관리
- `pjt/settings.py` 파일의 `TEMLATES`의 `DIRS` 추가

```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'pjt' / 'templates'],
        ...
    },
]
```

#### 2-2 STATIC files 설정

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

```python
STATICFILES_DIRS = [os.path.join(BASE_DIR, "pjt", "static")]
```

- `pjt/static/` 폴더 생성 후, 정적 파일 폴더별 관리
- `static/css` 폴더 생성 후, css 파일 관리

#### 2-3 기본 Templates 관리

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
    {% include 'header.html' %}
    {% block content %}{% endblock %}
    {% include 'footer.html' %}
  </body>

</html>
```

- `templates/header.html` 파일 생성

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
  <div class="container-fluid">
    <a class="navbar-brand"></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        {% if request.user.is_authenticated %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:detail' user.pk %}">{{ user }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="{% url 'accounts:logout' %}">로그아웃</a>
          </li>
        {% else %}
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="{% url 'accounts:signup' %}">회원가입</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'accounts:login' %}">로그인</a>
          </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
```

- `templates/footer.html` 파일 생성

```html
<footer class="m-0 p-3 bg-dark fixed-bottom">
  <div class="container-fluid">
    <p class="m-0 text-center text-light">© 2022 C.M.A</p>
  </div>
</footer>
```

#### 2-4 앱 Template 설정

- `앱이름/templates/앱이름` 폴더 생성 후, 템플릿 관리



### 3. 시작 페이지

#### 3-1. URL 설정

- `pjt/urls.py` 파일에 추가

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

- `pjt/views.py` 파일 생성

```python
from django.shortcuts import render

def index(request):

    return render(request, 'index.html')
```

#### 3-3. html 작성

- `pjt/templates/index.html` 파일 생성

```html
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
    <div class="card shadow">
      <div class="card-header bg-dark">
        <h1 class="text-light">
          <i class="bi bi-brightness-high"></i>
          Welcome
        </h1>
      </div>
      <div class="card-body box">
        <a class="red" href="">Login</a>
        <a class="yellow" href="">Signup</a>
        <a class="green" href="">Home</a>
      </div>
    </div>
  </body>
</html>
```



### 4. `accounts` App

#### 4-1. App 생성

```bash
# Django 앱 생성
python manage.py startapp accounts
```

#### 4-2. App 등록

- `pjt/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'accounts',
    ...
]
```

#### 4-3. URL 설정

> app 단위의 URL 관리

- `pjt/urls.py` 파일에 추가

```python
from django.contrib import admin
from django.urls import path, include

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

- 활용 : `accounts:index` -> `/accounts/`

  - Template에서 활용 예시

  ```html
  {% url 'accounts:index' %}
  ```

  - View에서 활용 예시

  ```python
  redirect('accounts:index')
  ```

#### 4-4. View 설정

- `accounts/views.py` 파일에 함수 생성

```python
from django.shortcuts import render

def index(request):

    return render(request, 'accounts/index.html')
```



### 5. `User` Model 정의

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

- `pjt/settings.py` 파일의  `AUTH_USER_MODEL` 설정

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
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)
```

##### (4) html 작성

- `accounts/signup.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  <div class="container">
    <div class="card shadow">
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
            <input class="btn btn-dark" type="submit" value="OK">
          </div>
        </form>
      </div>
    </div>
  </div>
{% endblock %}
```

##### (4)  페이지 연결

- `pjt/templates/index.html` 파일에 추가

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
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
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
  <div class="container">
    <div class="card shadow">
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
            <input class="btn btn-dark" type="submit" value="OK">
          </div>
        </form>
      </div>
    </div>
  </div>
{% endblock %}
```

##### (4)  페이지 연결

- `pjt/templates/index.html` 파일에 추가

```html
<a class="red" href="{% url 'accounts:login' %}">Login</a>
```

#### 6-3. 로그아웃 기능

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
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

...

def logout(request):
    auth_logout(request)
    return redirect('accounts:login')
```

##### (3)  페이지 연결

- `accounts/detail.html` 파일에 추가

```html
<a class="red" href="{% url 'accounts:logout' %}">Logout</a>
```

#### 6-4. 회원 목록 기능

##### (1) View 설정

- `accounts/views.py` 파일에 임포트 추가 및 함수 수

```python
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model

def index(request):
    users = get_user_model().objects.all()
    context = {
        'users': users
    }
    return render(request, 'accounts/index.html', context)
```

##### (3) html 작성

- `accounts/index.html` 파일 생성

```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block content %}
  {% include 'header.html' %}
  <div class="container">
    <div class="p-3 pt-5 d-flex flex-column align-items-center">
      <h1 class="m-0 p-3 text-center">회원 목록</h1>
      <div class="mb-3 d-flex w-100 justify-content-end">
        <a class="btn btn-dark" href="{% url 'accounts:signup' %}">회원가입</a>
      </div>
      <table class="table align-middle text-center table-borderless">
        <thead class="bg-dark text-light">
          <tr>
            <th scope="col" class="text-center">번호</th>
            <th scope="col" class="text-center">이름</th>
            <th scope="col" class="text-center">가입일</th>
          </tr>
        </thead>
        <tbody class="bg-light">
          {% for user in users %}
            <tr>
              <td class="text-center">{{ user.pk }}</td>
              <td class="text-center">
                <a class="text-dark" href="{% url 'accounts:detail' user.pk %}">{{ user.username }}</a>
              </td>
              <td class="text-center">{{ user.date_joined }}</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
  {% include 'footer.html' %}
{% endblock %}
```

#### 6-5. 회원 상세정보 기능

##### (1) URL 설정

- `accounts/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('signup/',  views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
```

##### (2) View 설정

- `accounts/views.py` 파일에 임포트 추가 및 함수 생성

```python
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
  <div class="container">
    <div class="box">
      <h1 class="">
        {{ user }}
        님의 프로필</h1>
      <dl class="row">
        <dt class="col-sm-2 text-center">이름</dt>
        <dd class="col-sm-10">{{ user.username }}</dd>
        <dt class="col-sm-2 text-center">가입일</dt>
        <dd class="col-sm-10">{{ user.date_joined }}</dd>
      </dl>
      {% if request.user.is_authenticated %}
        <a class="red" href="{% url 'accounts:logout' %}">Logout</a>
        <a class="yellow" href="{% url 'accounts:update' %}">Update</a>
      {% endif %}
    </div>
  </div>
{% endblock %}
```

#### 6-6. 회원 정보수정 기능

##### (1) CustomUserCreationForm 생성

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
    path('<int:pk>/', views.detail, name='detail'),
    path('signup/',  views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
]
```

##### (3) View 설정

- `accounts/views.py` 파일에 임포트 추가 및 함수 생성

```python
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
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
  <div class="container">
    <div class="card shadow">
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
            <input class="btn btn-dark" type="submit" value="OK">
          </div>
        </form>
      </div>
    </div>
  </div>
{% endblock %}
```

##### (5)  페이지 연결

- `accounts/detail.html` 파일에 추가

```html
<a class="yellow" href="{% url 'accounts:update' %}">Update</a>
```

