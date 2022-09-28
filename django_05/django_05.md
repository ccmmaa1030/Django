# Django 05



## CRUD 실습

### 0. 실습 준비

- 환경 설정

```bash
# 폴더 생성 및 이동
$ mkdir todo
$ cd todo/

# VS code 실행
$ code .

# 가상환경 생성 및 확인
$ python -m venv todo-venv
$ ls

# 가상환경 실행
$ source todo-venv/Scripts/activate
(todo-venv)

# Django LTS 버전, black 패키지 설치 및 확인
$ pip install django==3.2.13
$ pip install black
$ pip list

# Django 프로젝트 생성 및 확인
# todo 폴더 안에 프로젝트 config 생성
$ django-admin startproject config .
$ ls

# Django 앱 생성
# todo 폴더 안에 앱 todo 생성
python manage.py startapp todo

# 서버 정상 실행 확인
$ python manage.py runserver
# ctrl + c 눌러서 종료
```

- 실습 모델 정보

  - 모델 이름 : Todo
  - 모델 필드

  | 필드 이름  | 역할       | 필드    | 속성              |
  | ---------- | ---------- | ------- | ----------------- |
  | id         | 기본키     |         |                   |
  | content    | 할 일 내용 | Char    | max_length=80     |
  | completed  | 완료 여부  | Boolean | default=False     |
  | priority   | 우선순위   | Integer | default=3         |
  | created-at | 생성 날짜  | Date    | auto_now_add=True |
  | deadline   | 마감 기한  | Date    | null=True         |



### 1. `config/settings.py` 앱 등록

```py
# INSTALLED_APPS에 todo 등록
INSTALLED_APPS = [
    "todo",
     ...
]
```



### 2.  `config/urls.py` url 설정

- `path`, `include` import
- `urlpatterns`에 `path` 설정

```py
# path, includ import 하기
from django.contrib import admin
from django.urls import path, include

# urlpatterns에 path 설정
urlpatterns = [
    path("admin/", admin.site.urls),
    path("first/", include("first.urls")),
]
```



### 3. `todo/models.py` 파일 아래 모델 `Todo` 생성

- 모델 작성

```py
from pyexpat import model
from django.db import models


class Todo(models.Model):
    content = models.CharField(max_length=80)
    priority = models.IntegerField(default=3)
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



### 4. `todo/urls.py` 설정

- `todo/` 앱 아래 `urls.py` 파일 생성

- `app_name`을 `todo`로 설정

- `urlpatterns`에 `path` 설정

```py
from django.urls import path
from . import views

# app_name 설정
app_name = "todo"

# urlpatterns에 path 설정
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path("update/<int:pk>", views.update, name="update"),
]
```



### 5. `today/views.py` 설정

- `rendere`, `redirect` import
- `todo/models.py`에서 생성한 모델 `Todo` import

```py
from django.shortcuts import render, redirect
from .models import Todo
```

- C(CREATE) : 함수 create 생성

```py
def create(request):
    # 1. parameter로 날라온 데이터를 받아서
    content = request.GET.get("content")
    priority = int(request.GET.get("priority")) # 정수형으로 변환
    deadline = request.GET.get("deadline")

    # 2. DB에 저장
    Todo.objects.create(content=content, priority=priority, deadline=deadline)

    return redirect("todo:index")
```

- R(READ) : 함수 index 생성

```py
def index(request):
    # 1. id를 기준으로 오름차순으로 정렬한 모든 데이터를 받아서
    todos = Todo.objects.all().order_by("id")
	
    # 2. context 딕셔너리로 저장 후 전달
    context = {
        "todos": todos,
    }
    
    return render(request, "todo/index.html", context)
```

- U(UPDATE) : 함수 update 생성

```py
def update(request, pk):
    # pk에 해당하는 글 수정
    # 추후 추가
    return redirect("todo:index")
```

- D(DELETE) : 함수 delete 생성

```py
def delete(request, pk):
    # pk에 해당하는 글 삭제
    Todo.objects.get(id=pk).delete()
    return redirect("todo:index")
```



### 6. `todo/templates` 설정

- `todo/` 아래 `templates/todo/` 폴더 생성
- `todo/templates/todo/` 아래 `index.html` 파일 생성

> Bootstrap, Google Fonts 사용

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- CSS only -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
  <title>Document</title>
  <style>
    <!-- Google Font -->
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

    body {
      font-family: 'Nanum Gothic', sans-serif;
    }

    h1 {
      font-family: 'Jua', sans-serif;
    }
  </style>
</head>

<body>
    
  <!-- 할 일 추가하기 -->
    
  <!-- 할 일 목록보기 -->
  
  <!-- JavaScript Bundle with Popper -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
    crossorigin="anonymous"></script>
</body>

</html>
```

- 할 일 추가하기 : `<form>`
  - 할 일 : `<input type = "text">` 활용
  - 우선순위 : `<select>`, `<option>` 활용
  - 마감기한 : `<input type = "date">` 활용
  - 할 일 추가 버튼 : `<input type = "submit">` 활용

```html
  <!-- 할 일 추가하기 -->
  <div class="p-3 d-flex flex-column align-items-center">
    <h1 class="w-100 m-0 p-3 text-center">할 일 추가</h1>
    <form action="{% url 'todo:create' %}" class="w-100">
      <!-- content -->
      <div class="input-group mb-3">
        <span class="input-group-text" id="content-add">할 일</span>
        <input type="text" name="content" class="form-control" aria-describedby="content-add">
      </div>
      <!-- priority -->
      <div class="input-group mb-3">
        <label class="input-group-text" for="priority-add">우선순위</label>
        <select class="form-select" name="priority" id="priority-add">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
      </div>
      <!-- deadline -->
      <div class="input-group mb-3">
        <span class="input-group-text" id="deadline-add">마감기한</span>
        <input type="date" name="deadline" class="form-control" aria-describedby="deadline-add">
      </div>
      <!-- submit -->
      <input type="submit" value="할 일 추가" class="btn btn-outline-primary w-100">
    </form>
  </div>
```

- 할 일 목록 보기 : `<table>`
  - `<thead>` : 우선순위 / 할 일 / 생성 날짜 / 마감 기한 / 진행 상태 / 상태 변경 / 삭제 를 테이블 헤더로 사용
  - `<tbody>` : id를 기준으로 오름차순으로 정렬한 모든 데이터를 화면에 표시

```html
  <!-- 할 일 목록 보기 -->
  <div class="p-3 d-flex flex-column align-items-center">
    <h1 class="w-100 m-0 p-3 text-center">할 일 목록</h1>
    <table class="table">
      <thead>
        <tr>
          <th scope="col" class="text-center">우선순위</th>
          <th scope="col" class="text-center">할 일</th>
          <th scope="col" class="text-center">생성 날짜</th>
          <th scope="col" class="text-center">마감 기한</th>
          <th scope="col" class="text-center">진행 상태</th>
          <th scope="col" class="text-center">상태 변경</th>
          <th scope="col" class="text-center">삭제</th>
        </tr>
      </thead>
      <tbody>
        {% for todo in todos %}
        <tr>
          <td class="text-center">{{ todo.priority }}</td>
          <td>{{ todo.content }}</td>
          <td class="text-center">{{ todo.created_at }}</td>
          <td class="text-center">{{ todo.deadline }}</td>
          <td class="text-center">{{ todo.completed }}</td>
          <td class="text-center"><a href="/todo/update/{{ todo.id }}" class="btn btn-primary btn-sm">변경</a></td>
          <td class="text-center"><a href="/todo/delete/{{ todo.id }}" class="btn btn-danger btn-sm">삭제</a></td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
```

- 상태 변경하기
  - 버튼을 누르면 해당 할 일의 상태(True/False)가 수정됨

```html
<!-- 추후 추가 -->
```

- 할 일 삭제하기
  - 버튼을 누르면 해당 할 일이 삭제됨

```html
<a href="/todo/delete/{{ todo.id }}" class="btn btn-danger btn-sm">삭제</a>
```

