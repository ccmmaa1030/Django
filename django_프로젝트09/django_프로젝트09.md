# Django 프로젝트09



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
$ source venv/Scripts/activate
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
python manage.py startapp reviews
```

#### 2-2. App 등록

- `pjt/settings.py` 파일의 `INSTALLED_APPS`에 추가

```python
INSTALLED_APPS = [
    'reviews',
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
    path('reviews/', include('reviews.urls')),
]
```

- `reviews/urls.py` 파일 생성

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # GET : http://127.0.0.1:8000/reviews/
    path('', views.index, name='index'),
    # GET : http://127.0.0.1:8000/reviews/<int:pk>/
    # POST : http://127.0.0.1:8000/reviews/create/
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/update/
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/delete/
]
```

- 활용 : `reviews:index` -> `/reviews/`

  - Template에서 활용 예시

  ```html
  {% url 'reviews:index' %}
  ```

  - View에서 활용 예시

  ```python
  redirect('reviews:index')
  ```

#### 2-4. View 설정

- `reviews/views.py` 파일에 함수 생성

```python
from django.shortcuts import render, redirect

def index(request):
    ...
    return render(request, 'reviews/index.html')
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

- `reviews/static/reviews` 폴더 생성 후, 정적 파일 폴더별 관리
- `reviews/images` 폴더 생성 후, 이미지 정적 파일 관리

#### 3-4. 정적 파일 활용

- 사용자 정의 템플릿 태그 세트를 로드(load)

```html
{% load static %}
```

- 정적 파일 활용 예시

```html
<img src="{% static 'reviews/images/logo.png' %}" alt="로고 이미지">
```



### 4. Template 관리

#### 4-1 기본 Template 설정

- `templates` 폴더 생성 후, 템플릿 관리
- `pjt/settings.py` 파일의 `TEMPLATES`에 `DIRS` 설정

```python
TEMPLATES = [
    {
		...
        'DIRS': [BASE_DIR / 'templates'],
        ...
    },
]
```

- `templates/base.html` 파일 생성

```bash
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>영화 리뷰 커뮤니티</title>
    {% load bootstrap5 %}
    {% bootstrap_css %}
    {% bootstrap_javascript %}
    {% bootstrap_messages %}
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&display=swap');
      body {
        font-family: 'Do Hyeon', sans-serif;
      }
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css">
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

<nav class="navbar navbar-expand-lg navbar-dark bg-success">
  <div class="container-fluid">
    <a class="navbar-brand">
      <img src="{% static 'reviews/images/logo.png' %}" width="50" height="40" alt="logo image">
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="{% url 'reviews:index' %}">리뷰 목록</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{% url 'reviews:create' %}">리뷰 작성</a>
        </li>
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

#### 4-2 앱 Template 설정

- `reviews/templates/reviews` 폴더 생성 후, 템플릿 관리
- `reviews/index.html` 파일 생성



### 5. Model 정의

> DB 스키마 설계

#### 5-1. 클래스 정의

- `reviews/models.py` 파일에 클래스 추가

```python
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
    create_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
```

#### 5-2. 마이그레이션 파일 생성

- `reviews/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

#### 5-3. DB 반영

```bash
$ python manage.py migrate
```

#### 5-4 Model 활용

- `reviews/views.py` 파일에 임포트 추가

```python
from django.shortcuts import render, redirect
from .models import Review
...
```



### 6. CRUD 기능 구현

#### 6-0. ModelForm 선언

> 선언된 모델에 따른 필드 구성 (1) Form 생성 (2) 유효성 검사

- `reviews/forms.py` 파일 생성

```py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'content', 'movie_name', 'grade']
```

#### 6-1. 게시글 목록

> DB에서 게시글을 가져와서, template에 전달

- `reviews/views.py` 파일의 함수로 요청 처리

```python
def index(request):
    # DB에서 모든 리뷰 정보 가져옴 + pk의 내림차순 정렬
    reviews = Review.objects.order_by('-pk')
    # template에 전달
    context = {
        'reviews': reviews
    }
    # index 페이지로 이동
    return render(request, 'reviews/index.html', context)
```

- `reviews/index.html` 파일에 추가

```html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
  <div class="container">
    <div class="p-3 pt-5 d-flex flex-column align-items-center">
      <h1 class="m-0 p-3 text-center">영화 리뷰 게시판</h1>
      <div class="mb-3 d-flex w-100 justify-content-end">
        <form class="d-flex">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">
            <i class="bi bi-search"></i>
          </button>
        </form>
      </div>
      <table class="table align-middle text-center table-borderless">
        <thead class="bg-success text-light">
          <tr>
            <th scope="col">번호</th>
            <th scope="col">제목</th>
            <th scope="col">영화</th>
            <th scope="col">평점</th>
            <th scope="col">수정</th>
            <th scope="col">삭제</th>
          </tr>
        </thead>
        <tbody class="bg-light">
          {% for review in reviews %}
            <tr>
              <td>{{ review.pk }}</td>
              <td class="text-start">{{ review.title }}</td>
              <td>{{ review.movie_name }}</td>
              <td>{{ review.get_grade_display }}</td>
              <td>
                <a class="btn btn-primary btn-sm" href="">
                  <i class="bi bi-pencil-fill"></i>
                </a>
              </td>
              <td>
                <a class="btn btn-danger btn-sm" href="">
                  <i class="bi bi-trash-fill"></i>
                </a>
              </td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
      <div class="mt-3 d-flex w-100 justify-content-end">
        <a class="btn btn-outline-success" href="">
          <i class="bi bi-pencil-fill"></i>
        </a>
      </div>
    </div>
  </div>
{% endblock %}
```

#### 6-2 게시글 상세보기

> 게시글 목록에서 특정 게시글의 제목을 누르면 상세보기 페이지로 이동

- `reviews/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # GET : http://127.0.0.1:8000/reviews/
    path('', views.index, name='index'),
    # GET : http://127.0.0.1:8000/reviews/<int:pk>/
    path('<int:pk>/', views.detail, name='detail'),
    # POST : http://127.0.0.1:8000/reviews/create/
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/update/
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/delete/
]
```

- `reviews/views.py` 파일의 함수로 요청 처리

```python
def detail(request, pk):
    # DB에서 특정 리뷰 정보 하나만 가져옴
    review = Review.objects.get(pk=pk)
    # template에 전달
    context = {
        'review': review
    }
    # detail 페이지로 이동
    return render(request, 'reviews/detail.html', context)
```

- `reviews/index.html` 파일에 추가

```html
<td class="text-start">
	<a href="{% url 'reviews:detail' review.pk %}">{{ review.title }}</a>
</td>
```

- `reviews/detail.html` 파일 생성

```html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
  <div class="container">
    <div class="p-3 pt-5 d-flex flex-column align-items-center">
      <h1 class="m-0 p-3 fw-bold display-5 text-center">{{ review.title }}</h1>
      <dl class="row">
        <dt class="col-sm-2 text-center">영화</dt>
        <dd class="col-sm-10">{{ review.movie_name }}</dd>
        <dt class="col-sm-2 text-center">평점</dt>
        <dd class="col-sm-10">{{ review.grade }}점 {{ review.get_grade_display }}</dd>
        <dt class="col-sm-2 text-center">리뷰</dt>
        <dd class="col-sm-10">{{ review.content }}</dd>
        <dt class="col-sm-2 text-center">작성일</dt>
        <dd class="col-sm-10">{{ review.create_at | date:"Y-m-d" }}</dd>
        <dt class="col-sm-2 text-center">수정일</dt>
        <dd class="col-sm-10">{{ review.updated_at | date:"Y-m-d" }}</dd>
      </dl>
      <div class="d-flex w-100 justify-content-end">
        <a class="btn btn-primary mx-2" href="">
          <i class="bi bi-pencil-fill"></i>
        </a>
        <a class="btn btn-danger" href="">
          <i class="bi bi-trash-fill"></i>
        </a>
      </div>
    </div>
  </div>
{% endblock %}
```

#### 6-3 게시글 생성

> 기존 new, create -> ModelForm 로직 create로 변경
>
> 생성 버튼 누르면 게시글 생성 페이지로 이동

##### (1) HTML Form 제공 (GET)

- `reviews/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # GET : http://127.0.0.1:8000/reviews/
    path('', views.index, name='index'),
    # GET : http://127.0.0.1:8000/reviews/<int:pk>/
    path('<int:pk>/', views.detail, name='detail'),
    # POST : http://127.0.0.1:8000/reviews/create/
    path('create/', views.create, name='create'),
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/update/
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/delete/
]
```

- `reviews/views.py` 파일에 임포트 추가 및 함수 생성

```python
...
from .forms import ReviewForm

def create(request):
    # ModelForm
    review_form = ReviewForm()
    # template에 전달
    context = {
        'review_form': review_form
    }
    # create 페이지로 이동
    return render(request, 'reviews/create.html', context=context)
```

- `reviews/index.html` 파일에 추가

```html
<div class="mt-3 d-flex w-100 justify-content-end">
	<a class="btn btn-outline-success" href="{% url 'reviews:create' %}">
		<i class="bi bi-pencil-fill"></i>
	</a>
</div>
```

- `reviews/create.html` 파일 생성
  - HTML Form 태그 활용 : 어떤 필드로 구성할 것인가(`name`, `value`) / 어디로 보낼 것인가(`action`, `method`)

```html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
  <div class="container">
    <div class="p-3 pt-5">
      <h1 class="m-0 p-3 text-center">리뷰 작성</h1>
      <form action="" method="POST">
        <!-- POST 요청에서 CSRF 공격 방어 : 전송된 token의 유효성 검증 -->
        {% csrf_token %}
        <!-- Bootstrap 적용 ModleForm -->
        {% bootstrap_form review_form %}
        <button class="btn btn-success" type="submit">
          <i class="bi bi-pencil-fill"></i>
        </button>
      </form>
    </div>
  </div>
{% endblock %}
```

##### (2) 입력받은 데이터 처리 (POST)

> 게시글 DB에 생성하고 index 페이지로 redirect

- `reviews/views.py` 파일의 함수로 요청 처리

```python
def create(request):
    # POST 요청 처리
    if request.method == 'POST':
        # ModelForm에서 입력받은 데이터
        review_form = ReviewForm(request.POST)
        # 유효성 검사를 통과하면
        if review_form.is_valid():
            # DB에 저장
            review_form.save()
            # index 페이지로 이동
            return redirect('reviews:index')
    # GET 요청 처리
    else:
        # ModelForm
        review_form = ReviewForm()
    # template에 전달
    context = {
        'review_form': review_form
    }
    # create 페이지로 이동
    return render(request, 'reviews/create.html', context=context)
```

#### 6-4 게시글 수정

> 수정 버튼을 누르면 특정 게시글의 수정 페이지로 이동

##### (1) HTML Form 제공 (GET)

> 사용자에게 수정할 수 있는 양식 제공

- `reviews/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # GET : http://127.0.0.1:8000/reviews/
    path('', views.index, name='index'),
    # GET : http://127.0.0.1:8000/reviews/<int:pk>/
    path('<int:pk>/', views.detail, name='detail'),
    # POST : http://127.0.0.1:8000/reviews/create/
    path('create/', views.create, name='create'),
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/update/
    path('<int:pk>/update/', views.update, name='update'),
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/delete/
]
```

- `reviews/views.py` 파일에 임포트 추가 및 함수 생성

```python
def update(request, pk):
    # DB에서 특정 리뷰 정보 하나만 가져옴
    review = Review.objects.get(pk=pk)
    # 특정 리뷰 정보를 ModelForm에 입력
    review_form = ReviewForm(instance=review)
    # template에 전달
    context = {
        'review_form': review_form
    }
    # update 페이지로 이동
    return render(request, 'reviews/update.html', context=context)
```

- `reviews/update.html` 파일 생성
  - HTML Form 태그 활용 : 어떤 필드로 구성할 것인가(`name`, `value`) / 어디로 보낼 것인가(`action`, `method`)

```html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
  <div class="container">
    <div class="p-3 pt-5">
      <h1 class="m-0 p-3 text-center">리뷰 수정</h1>
      <form action="" method="POST">
        <!-- POST 요청에서 CSRF 공격 방어 : 전송된 token의 유효성 검증 -->
        {% csrf_token %}
        <!-- Bootstrap 적용 ModleForm -->
        {% bootstrap_form review_form %}
        <button class="btn btn-success" type="submit">
          <i class="bi bi-pencil-fill"></i>
        </button>
      </form>
    </div>
  </div>
{% endblock %}
```

##### (2) 입력받은 데이터 처리 (POST)

> 기존 edit, update -> ModelForm 로직 update로 변경
>
> 특정 게시글 수정고 index 페이지로 redirect

- `reviews/views.py` 파일의 함수로 요청 처리

```python
def update(request, pk):
    # DB에서 특정 리뷰 정보 하나만 가져옴
    review = Review.objects.get(pk=pk)
    # POST 요청 처리
    if request.method == 'POST':
        # ModelForm에서 입력받은 데이터
        review_form = ReviewForm(request.POST, instance=review)
        # 유효성 검사를 통과하면
        if review_form.is_valid():
            # DB에 저장
            review_form.save()
            # detail 페이지로 이동
            return redirect('reviews:detail', review.pk)
    # GET 요청 처리
    else:
        # 특정 리뷰 정보를 ModelForm에 입력
        review_form = ReviewForm(instance=review)
    # template에 전달
    context = {
        'review_form': review_form
    }
    # update 페이지로 이동
    return render(request, 'reviews/update.html', context=context)
```

- `reviews/index.html`, `reviews/detail.html` 파일에 추가

```html
<a class="btn btn-primary btn-sm" href="{% url 'reviews:update' review.pk %}">
	<i class="bi bi-pencil-fill"></i>
</a>
```

#### 6-5 게시글 삭제

> 삭제 버튼을 누르면 해당 게시글 삭제

- `reviews/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # GET : http://127.0.0.1:8000/reviews/
    path('', views.index, name='index'),
    # GET : http://127.0.0.1:8000/reviews/<int:pk>/
    path('<int:pk>/', views.detail, name='detail'),
    # POST : http://127.0.0.1:8000/reviews/create/
    path('create/', views.create, name='create'),
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/update/
    path('<int:pk>/update/', views.update, name='update'),
    # POST : http://127.0.0.1:8000/reviews/<int:pk>/delete/
    path('<int:pk>/delete/', views.delete, name='delete'),
]
```

- `reviews/views.py` 파일의 함수로 요청 처리

```python
def delete(request, pk):
    # DB에서 특정 리뷰 정보 하나만 가져옴
    review = Review.objects.get(pk=pk)
    # 리뷰 삭제
    review.delete()
    # index 페이지로 이동
    return redirect('reviews:index')
```

- `reviews/index.html`, `reviews/detail.html` 파일에 추가

```html
<a class="btn btn-danger" href="{% url 'reviews:delete' review.pk %}">
	<i class="bi bi-trash-fill"></i>
</a>
```



### 추가 기능 아이디어

- 검색 기능 (https://integer-ji.tistory.com/10?category=745989)
- 좋아요 기능
- 조회수 기능
- 게시판 페이지네이션 기능
- 회원가입 기능

