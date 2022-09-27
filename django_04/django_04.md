# Django 04



## 오전 - 폴더 관리(Tamplates, App 분리)

### 0. 실습 준비

- 환경 설정

```bash
# 폴더 생성 및 이동
$ mkdir today
$ cd today/

# 가상환경 생성 및 확인
$ python -m venv today-venv
$ ls

# 가상환경 실행
$ source today-venv/Scripts/activate
(today-venv)

# Django LTS 버전, black 패키지 설치 및 확인
$ pip install django==3.2.13
$ pip install black
$ pip list

# Django 프로젝트 생성 및 확인
# today 폴더 안에 프로젝트 todaypjt 생성
$ django-admin startproject todaypjt .
$ ls

# Django 앱 생성
# today 폴더 안에 앱 first, second 2개 생성
python manage.py startapp first
python manage.py startapp second

# 서버 정상 실행 확인
$ python manage.py runserver
# ctrl + c 눌러서 종료

# VS code 실행
$ code .
```



### 1. `todaypjt/settings.py` 앱 등록

```py
# INSTALLED_APPS에 first, second 등록
INSTALLED_APPS = [
    "first",
    "second",
      ...
]
```



### 2.  `todaypjt/urls.py` url 설정

```py
                ...
# path, includ import 하기
from django.urls import path, include

# urlpatterns에 path 설정
urlpatterns = [
                ...
    path("first/", include("first.urls")),
    path("second/", include("second.urls")),
]
```



### 3. 기본 `templates` 설정

- `today/` 아래 `templates/` 폴더 생성 후 `base.html` 파일 생성

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  {% block content %}
  {% endblock %}
</body>
</html>
```

- `today/templates/base.html` 템플릿 경로 설정

```py
# TEMPLATES의 "DIRS"에 절대경로 지정
TEMPLATES = [
	{    
                      ...
        "DIRS": [BASE_DIR / "templates"],
                      ...
    },
]
```



### 4. `first` 앱 `urls`, `views`, `templates`설정

- `first/` 아래 `urls.py` 파일 생성

- `first/urls.py` url 설정

```py
from django.urls import path
from . import views

# urlpatterns에 path 설정
urlpatterns = [
    path("", views.index),
]
```

- `first/views.py` 함수 설정

```py
from django.shortcuts import render

def index(request):
    return render(request, "first/index.html")
```

- `first/` 아래 `templates/first/` 폴더 생성
- `first/templates/first/` 아래 `index.html` 파일 생성

```html
<!-- base.html 상속 -->
{% extends 'base.html' %}

{% block content %}

<!-- 내용 작성 -->

{% endblock %}
```



### 5. `second` 앱 `urls`, `views`, `templates`설정

- `second/` 아래 `urls.py` 파일 생성

- `second/urls.py` url 설정

```py
from django.urls import path
from . import views

# urlpatterns에 path 설정
urlpatterns = [
    path("index/", views.index),
    path("ping/", views.ping),
    path("pong/", views.pong),
]
```

- `first/views.py` 함수 설정

```py
from django.shortcuts import render

def index(request):
    return render(request, "second/index.html")

def ping(request):
    return render(request, "second/ping.html")

def pong(request):
    return render(request, "second/pong.html")
```

- `second/` 아래 `templates/second/` 폴더 생성
- `second/templates/second/` 아래 `index.html`, `ping.html`, `pong.html` 파일 생성

```html
<!-- base.html 상속 -->
{% extends 'base.html' %}

{% block content %}

<!-- 내용 작성 -->

{% endblock %}
```



## 오후 - ORM

### 0. 실습 준비

- 환경 설정

```bash
# todo.zip 실습파일 압축 해제
# TODO 폴더 안에 이미 프로젝트 config, 앱 todo 생성되어 있음

# 가상환경 생성 및 실행
$ python -m venv todo-venv
$ source todo-venv/Scripts/activate
(todo-venv)

# 패키지 설치
$ pip install -r requirements.txt

# 서버 정상 실행 확인
$ python manage.py runserver
# ctrl + c 눌러서 종료

# shell_plus 진입
$ python manage.py shell_plus
```

- 실습 모델 정보

  - 모델 이름 : Todo
  - 모델 필드

  | 필드 이름  | 역할       | 필드    | 속성              |
  | ---------- | ---------- | ------- | ----------------- |
  | id         | 기본키     |         |                   |
  | content    | 할 일 내용 | Char    | max_length=80     |
  | completed  | 완료 여부  | Boolean | default=False     |
  | priority   | 우선순위   | Integer |                   |
  | created-at | 생성 날짜  | Date    | auto_now_add=True |
  | deadline   | 마감 기한  | Date    | null=True         |



### 1. `todo/models.py` 파일 아래 모델 `Todo`

> todo.zip에 모델 작성/마이그레이트가 이미 완료되어 있으므로 할 필요 없음

- 모델 작성

```py
from django.db import models

class Todo(models.Model):
    content = models.CharField(max_length=80)
    priority = models.IntegerField()
    completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True)
```

- 모델 마이그레이트

```bash
(todo-venv)
# 가상환경 실행 후 터미널에 입력
$ python manage.py makemigrations
$ python manage.py migrate
```



### 2. 실습 문제 풀이

> shell_plus 진입 후 문제 풀이 진행

- 아래 내용의 데이터 추가하기
  - content: 실습 제출, priority: 5, deadline: 2022-09-27

```py
Todo.objects.create(content='실습 제출', priority=5, deadline='2022-09-27')
```

- 모든 데이터를 id 기준으로 오름차순 정렬해서 가져오기

```py
todos = Todo.objects.all().order_by('id')
```

- 모든 데이터를 deadline 기준으로 내림차순 정렬해서 가져오기

```py
todos = Todo.objects.all().order_by('-deadline')
```

- 모든 데이터를 priority가 높은 순으로 정렬해서 가져오기

```py
todos = Todo.objects.all().order_by('-priority')
```

- priority가 5인 모든 데이터를 id 기준으로 오름차순 정렬해서 가져오기

```py
todos = Todo.objects.filter(priority=5).order_by('id')
```

- completed가 True인 모든 데이터를 id 기준으로 오름차순 정렬해서 가져오기

```py
todos = Todo.objects.filter(completed=True).order_by('id')
```

- priority가 5인 데이터의 개수

```py
count = Todo.objects.filter(priority=5).count()
```

- id가 1인 데이터 1개 가져오기

```py
todo = Todo.objects.get(id=1)
```

- id가 1인 데이터 삭제하기

```py
todo = Todo.objects.get(id=1)
todo.delete()
```

- id가 10인 데이터의 priority 값을 5로 변경하기

```py
todo = Todo.objects.get(id=10)
todo.priority = 5
todo.save()
```

