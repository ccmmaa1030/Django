# Django 09



## Django CRUD

> Django : 파이썬 기반 웹 프레임워크



### 1. 환경 설정

#### 1-1. 가상환경 생성 및 실행

> 가상환경 : 프로젝트별 별도 패키지 관리

```bash
# 가상환경 생성
$ python -m venv venv

# 가상환경 폴더 생성 확인
$ ls

# 가상환경 실행
$ source pjt-venv/Scripts/activate
(venv)
```

#### 1-2. Django, 추가 패키지 설치 및 기록

> 가상환경 실행한 상태에서 패키지 설치

```bash
# Django LTS 버전 설치
$ pip install django==3.2.13

# black 패키지 설치
$ pip install black

# Bootstrap 패키지 설치
$ pip install django-bootstrap-v5

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
python manage.py startapp movies
```

#### 2-2. App 등록

- `pjt/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'movies',
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
    path('articles/', include('movies.urls')),
]
```

- `articles/urls.py` 파일 생성

```python
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    ...
]
```

- 활용 : `articles:index` -> `/articles/`

  - Template에서 활용 예시

  ```html
  {% url 'movies:index' %}
  ```

  - View에서 활용 예시

  ```python
  redirect('movies:index')
  ```

#### 2-4. View 설정

- `articles/views.py` 파일에 함수 생성

```python
from django.shortcuts import render, redirect

def index(request):
    ...
    return render(request, 'movies/index.html')
```

### 3. Django Bootstrap 및 Static Files

#### 3-1 Bootstrap 등록

- `pjt/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'bootstrap5',
    ...
]
```

#### 3-2. STATIC files 설정

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

#### 3-3. 정적 파일 저장

- `movies/static/movies` 폴더 생성 후, 정적 파일 폴더별 관리
- `movies/images` 폴더 생성 후, 이미지 정적 파일 관리

#### 3-4. 정적 파일 활용

- 사용자 정의 템플릿 태그 세트를 로드(load)

```html
{% load static %}
```

- 정적 파일 활용 예시

```html
<img src="{% static 'movies/images/logo.png' %}" alt="로고 이미지">
```



### 4. Template 관리

#### 4-1 기본 Template 설정

- `templates` 폴더 생성 후, 템플릿 관리
- `templates/base.html` 파일 생성

```bash
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% load bootstrap5 %}
    {% bootstrap_css %}
    {% bootstrap_javascript %}
    {% bootstrap_messages %}
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
{% load static %}

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    ...
    <a class="navbar-brand">
      <img src="{% static 'movies/images/logo.png' %}" width="50" height="40" alt="logo image">
    </a>
    ...
</nav>
```

- `templates/footer.html` 파일 생성

#### 4-2 앱 Template 설정

- `movies/templates/movies` 폴더 생성 후, 템플릿 관리
- `movies/index.html` 파일 생성



### 5. Model 정의

> DB 스키마 설계

#### 5-1. 클래스 정의

- `movies/models.py` 파일에 클래스 추가

```python
class Movie(models.Model):
    title = models.CharField(max_length=20)
    summary = models.TextField()
    running_time = models.IntegerField()
    director = models.CharField(max_length=20)
    genre = models.CharField(max_length=20)
    opening_date = models.DateField()
```

#### 5-2. 마이그레이션 파일 생성

- `movies/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

#### 5-3. DB 반영

```bash
$ python manage.py migrate
```

#### 5-4 Model 활용

- `movies/views.py` 파일에 임포트 추가

```python
from django.shortcuts import render, redirect
from .models import Movie
...
```



### 6. CRUD 기능 구현

#### 6-0. ModelForm 선언

> 선언된 모델에 따른 필드 구성 (1) Form 생성 (2) 유효성 검사

- `movies/forms.py` 파일 생성

```py
from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = ['title', 'summary', 'running_time', 'director', 'genre', 'opening_date']
```

#### 6-1 게시글 생성

> 기존 new, create -> ModelForm 로직 create로 변경
>
> 생성 버튼 누르면 게시글 생성 페이지로 이동

##### (1) HTML Form 제공 (GET)

- `movies/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    ...
]
```

- `movies/views.py` 파일에 임포트 추가 및 함수 생성

```python
...
from .forms import MovieForm
...

def create(request):
    # ModelForm
    movie_form = MovieForm()
    # template에 전달
    context = {
        'movie_form': movie_form
    }
    # create 페이지로 이동
    return render(request, 'movies/create.html', context=context)
```

- `movies/index.html` 파일에 추가

```html
<a href="{% url 'movies:create' %}">글 쓰기</a>
```

- `movies/create.html` 파일 생성
  - HTML Form 태그 활용 : 어떤 필드로 구성할 것인가(`name`, `value`) / 어디로 보낼 것인가(`action`, `method`)

```html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
  <div class="container">
    <form action="" method="POST">
      <!-- POST 요청에서 CSRF 공격 방어 : 전송된 token의 유효성 검증 -->
      {% csrf_token %}
      <!-- Bootstrap 적용 ModleForm -->
      {% bootstrap_form movie_form %}
      <input class="btn btn-primary" type="submit" value="글 쓰기">
    </form>
  </div>
{% endblock %}
```

##### (2) 입력받은 데이터 처리 (POST)

> 게시글 DB에 생성하고 index 페이지로 redirect

- `movies/views.py` 파일의 함수로 요청 처리

```python
def create(request):
    # POST 요청 처리
    if request.method == 'POST':
        # ModelForm에서 입력받은 데이터
        movie_form = MovieForm(request.POST)
        # 유효성 검사를 통과하면
        if movie_form.is_valid():
            # DB에 저장
            movie_form.save()
            # index 페이지로 redirect
            return redirect('movies:index')
    # GET 요청 처리
    else:
        # ModelForm
        movie_form = MovieForm()
    # template에 전달
    context = {
        'movie_form': movie_form
    }
    # create 페이지로 이동
    return render(request, 'movies/create.html', context=context)
```

#### 6-2 게시글 목록

> DB에서 게시글을 가져와서, template에 전달

- `movies/views.py` 파일의 함수로 요청 처리

```python
def index(request):
    # DB에서 영화정보 가져옴 + pk의 내림차순으로 정렬
    movies = Movie.objects.order_by('-pk')
    # template에 전달
    context = {
        'movies': movies
    }
    # index 페이지로 이동
    return render(request, 'movies/index.html', context)
```

- `movies/index.html` 파일에 추가

```html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
  <div class="container">
    <!-- 영화 목록 -->
    <div class="p-3 pt-5 d-flex flex-column align-items-center">
      <h1 class="m-0 p-3 text-center">영화 게시판</h1>
      <div class="mb-3 d-flex w-100 justify-content-end">
        <a class="btn btn-primary" href="{% url 'movies:create' %}">글 쓰기</a>
      </div>
      <table class="table align-middle">
        <thead>
          <tr>
            <th scope="col" class="text-center">번호</th>
            <th scope="col" class="text-center">제목</th>
            <th scope="col" class="text-center">장르</th>
            <th scope="col" class="text-center">러닝타임</th>
            <th scope="col" class="text-center">수정</th>
            <th scope="col" class="text-center">삭제</th>
          </tr>
        </thead>
        <tbody>
          {% for movie in movies %}
            <tr>
              <td class="text-center">{{ movie.pk }}</td>
              <td class="text-center">
                <a href="{% url 'movies:detail' movie.pk %}">{{ movie.title }}</a>
              </td>
              <td class="text-center">{{ movie.genre }}</td>
              <td class="text-center">{{ movie.running_time }}분</td>
              <!-- 수정 -->
              <td class="text-center">
                <a class="btn btn-primary btn-sm" href="{% url 'movies:update' movie.pk %}">수정</a>
              </td>
              <!-- 삭제 -->
              <td class="text-center">
                <a class="btn btn-danger btn-sm" href="{% url 'movies:delete' movie.pk %}">삭제</a>
              </td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
{% endblock %}
```

#### 6-3 게시글 상세보기

> 게시글 목록에서 특정 게시글의 제목을 누르면 상세보기 페이지로 이동

- `movies/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>', views.detail, name='detail'),
    ...
]
```

- `movies/views.py` 파일의 함수로 요청 처리

```python
def detail(request, pk):
    # DB에서 특정 영화정보 하나만 가져옴
    movie = Movie.objects.get(pk=pk)
    # template에 전달
    context = {
        'movie': movie
    }
    # detail 페이지로 이동
    return render(request, 'movies/detail.html', context)
```

- `movies/index.html` 파일에 추가

```html
<td class="text-center">
    <!-- <a> 태그 이용해서 링크 설정 -->
    <a href="{% url 'movies:detail' movie.pk %}">{{ movie.title }}</a>
</td>
```

- `movies/detail.html` 파일 생성

```html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
  <div class="container">
    <div class="p-3 pt-5 d-flex flex-column align-items-center">
      <h1 class="m-0 p-3 fw-bold display-5 text-center">{{ movie.title }}</h1>
      <dl class="row">
        <dt class="col-sm-2 text-center">감독</dt>
        <dd class="col-sm-10">{{ movie.director }}</dd>
        <dt class="col-sm-2 text-center">장르</dt>
        <dd class="col-sm-10">{{ movie.genre }}</dd>
        <dt class="col-sm-2 text-center">개봉일</dt>
        <dd class="col-sm-10">{{ movie.opening_date }}</dd>
        <dt class="col-sm-2 text-center">러닝타임</dt>
        <dd class="col-sm-10">{{ movie.running_time }}분</dd>
        <dt class="col-sm-2 text-center">줄거리</dt>
        <dd class="col-sm-10">{{ movie.summary }}</dd>
      </dl>
      <div class="d-flex w-100 justify-content-end">
        <!-- 수정 -->
        <a class="btn btn-primary mx-2" href="{% url 'movies:update' movie.pk %}">수정</a>
        <!-- 삭제 -->
        <a class="btn btn-danger" href="{% url 'movies:delete' movie.pk %}">삭제</a>
      </div>
    </div>
  </div>
{% endblock %}
```

#### 6-4 게시글 삭제

> 삭제 버튼을 누르면 해당 게시글 삭제

- `movies/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    ...
]
```

- `movies/views.py` 파일의 함수로 요청 처리

```python
def delete(request, pk):
    # DB에서 특정 영화정보 하나만 가져옴
    movie = Movie.objects.get(pk=pk)
    # DB 삭제
    movie.delete()
    # index 페이지로 이동
    return redirect('movies:index')
```

- `movies/index.html`, `movies/detail.html` 파일에 추가

```html
<td class="text-center">
    <!-- <a> 태그 이용해서 링크 설정 -->
    <a class="btn btn-danger btn-sm" href="{% url 'movies:delete' movie.pk %}">삭제</a>
</td>
```

#### 6-5 게시글 수정

> 수정 버튼을 누르면 특정 게시글의 수정 페이지로 이동

##### (1) HTML Form 제공 (GET)

> 사용자에게 수정할 수 있는 양식 제공

- `movies/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
]
```

- `movies/views.py` 파일에 임포트 추가 및 함수 생성

```python
def update(request, pk):
    # DB에서 특정 영화정보 하나만 가져옴
    movie = Movie.objects.get(pk=pk)
    # 특정 영화정보 데이터를 form에 입력
    movie_form = MovieForm(instance=movie)
    # template에 전달
    context = {
        'movie_form': movie_form
    }
    # update 페이지로 이동
    return render(request, 'movies/update.html', context=context)
```

- `movies/update.html` 파일 생성
  - HTML Form 태그 활용 : 어떤 필드로 구성할 것인가(`name`, `value`) / 어디로 보낼 것인가(`action`, `method`)

```html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
  <div class="container">
    <form action="" method="POST">
      <!-- POST 요청에서 CSRF 공격 방어 : 전송된 token의 유효성 검증 -->
      {% csrf_token %}
      <!-- Bootstrap 적용 ModleForm -->
      {% bootstrap_form movie_form %}
      <input class="btn btn-primary" type="submit" value="글 수정">
    </form>
  </div>
{% endblock %}
```

##### (2) 입력받은 데이터 처리 (POST)

> 기존 edit, update -> ModelForm 로직 update로 변경
>
> 특정 게시글 수정고 index 페이지로 redirect

- `movies/views.py` 파일의 함수로 요청 처리

```python
def update(request, pk):
    # DB에서 특정 영화정보 하나만 가져옴
    movie = Movie.objects.get(pk=pk)
    # POST 요청 처리
    if request.method == 'POST':
        # ModelForm에서 입력받은 데이터
        movie_form = MovieForm(request.POST, instance=movie)
        # 유효성 검사를 통과하면
        if movie_form.is_valid():
            # DB에 저장
            movie_form.save()
            # detail 페이지로 redirect
            return redirect('movies:detail', movie.pk)
    # GET 요청 처리
    else:
        # ModelForm
        movie_form = MovieForm(instance=movie)
    # template에 전달
    context = {
        'movie_form': movie_form
    }
    # update 페이지로 이동
    return render(request, 'movies/update.html', context)
```

- `movies/index.html`, `movies/detail.html` 파일에 추가

```html
<td class="text-center">
    <!-- <a> 태그 이용해서 링크 설정 -->
    <a class="btn btn-danger btn-sm" href="{% url 'movies:update' movie.pk %}">삭제</a>
</td>
```



### 7. Admin site

> 사용자가 아닌 서버 관리자가 활용하기 위한 페이지로, 모델 클래스를 admin.py에 등록하고 관리

#### 7-1. admin 계정 생성

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

#### 7-2. admin site 접속 후 로그인

- http://127.0.0.1:8000/admin/ 로 접속 후 로그인

#### 7-3. Model 클래스 등록

- `articles/admin.py` 파일에 임포트 추가 및 클래스 추가

```python
from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    fields = ['title']

admin.site.register(Movie, MovieAdmin)
```
