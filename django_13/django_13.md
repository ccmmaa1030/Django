# Django 13



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
      <a class="red click" href="">Login</a>
      <a class="yellow click" href="">Signup</a>
      <a class="green click" href="">Member</a>
      <a class="blue click" href="">Home</a>
    </div>
  </div>
{% endblock %}
```



### 4. articles App

#### 4-1. App 생성

```bash
# Django 앱 생성
python manage.py startapp articles
```

#### 4-2. App 등록

- `config/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'articles',
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

#### 4-4. View 설정

- `articles/views.py` 파일에 함수 생성

```python
from django.shortcuts import render

def index(request):

    return render(request, 'articles/index.html')
```

#### 4-5. Templates 관리

- `articles/templates/articles` 폴더 생성 후, 템플릿 관리
- `articles/index.html` 파일 생성



### 5. Article Model 정의

#### 5-1. 클래스 정의

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

#### 5-2. 마이그레이션 파일 생성

- `articles/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

#### 5-3. DB 반영

```bash
$ python manage.py migrate
```



### 6. CRUD 기능 구현

#### 6-1. 게시글 작성 기능

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
from .forms import ArticleForm

...

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

#### 6-2. 게시글 목록 기능

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
    <div class="card-footer left my-2">
      <a class="red click" href="{% url 'articles:create' %}">글 작성</a>
    </div>

    <div class="row">
      {% for article in articles %}
        <div class="col-4">
          <div class="card">
            <img src="{{ article.image.url }}" class="card-img-top" alt="thumbnail">
            <div class="card-body">
              <a class="text-dark fs-4 fw-bold mx-0" href="{% url 'articles:detail' article.pk %}">
                {{ article.pk }}번 :
                {{ article.title }}</a>
              <p>{{ article.created_at | date:"Y-m-d" }}</p>
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

#### 6-3. 게시글 상세보기 기능

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
  <div class="card shadow w-50">
    <div class="card-header bg-dark">
      <h1 class="text-light">
        <i class="bi bi-card-list"></i>
        {{ article.pk }}번 게시글
      </h1>
    </div>
    <div class="card-body box">
      <dl class="row">
        <img src="{{ article.image.url }}" alt="{{ article.image }}" ">
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
      <a class="red click mx-2" href="">글 수정</a>
      <a class="blue click" href="">글 삭제</a>
    </div>
  </div>
{% endblock %}
```

##### (4) 페이지 연결

- `articles/index.html` 파일에 추가

```html
<a class="text-dark" href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
```

#### 6-4. 게시글 수정 기능

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
<a class="red click" href="{% url 'articles:update' article.pk %}">글 수정</a>
```

#### 6-5. 게시글 삭제 기능

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

def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')
```

##### (3) 페이지 연결

- `reviews/detail.html` 파일에 추가

```html
<a class="blue click" href="{% url 'articles:delete' article.pk %}">글 삭제</a>
```



### 7. Header & Footer

#### 7-1. Header

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
          <a class="nav-link" href="{% url 'articles:create' %}">글 작성하기</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

#### 7-2. Footer

- `config/templates/footer.html` 파일 생성

```html
<footer class="m-0 p-3 bg-dark fixed-bottom">
  <div class="container-fluid">
    <p class="m-0 text-center text-light">© 2022 C.M.A</p>
  </div>
</footer>
```

#### 7-3. 활용

- 필요한 페이지마다 추가

```html
{% include 'header.html' %}
{% include 'footer.html' %}
```
