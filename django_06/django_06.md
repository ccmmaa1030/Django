# Django 06



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



### 3. `base templates` 설정

- `TODO/` 아래 `templates/` 폴더 생성 후 `base.html` 파일 생성

> Bootstrap, Google Fonts 사용

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css">
  <title>Document</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

    body {
      font-family: 'Nanum Gothic', sans-serif;
    }

    .h-font {
      font-family: 'Jua', sans-serif;
    }
  </style>
</head>

<body>
  {% block content %}
  {% endblock %}
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
    crossorigin="anonymous"></script>
</body>

</html>
```

- `config/settings.py` 템플릿 경로 설정

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



### 4. `todo/models.py` 파일 아래 모델 `Todo` 생성

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



### 5. `todo/urls.py` 설정

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
    path("check/<int:pk>", views.check, name="check"),
    path("edit/<int:pk>", views.edit, name="edit"),
    path("update/<int:pk>", views.update, name="update"),
]
```



### 6. `today/views.py` 설정

- `rendere`, `redirect` import
- `todo/models.py`에서 생성한 모델 `Todo` import
- 오늘 날짜 데이터를 받아오기 위해 `datetime` import

```py
from django.shortcuts import render, redirect
from .models import Todo
from datetime import datetime
```

- C(CREATE) : 할 일 추가하기

```py
def create(request):
    # 1. parameter로 날라온 데이터를 받아서
    content = request.GET.get("content")
    # 우선순위 형변환해서 맞춤
    priority = int(request.GET.get("priority"))
    deadline = request.GET.get("deadline")

    # 2. DB에 저장
    Todo.objects.create(content=content, priority=priority, deadline=deadline)

    return redirect("todo:index")
```

- R(READ) : 기본 페이지 `Todo` 모델 데이터 읽음

```py
def index(request):
    todos = Todo.objects.all().order_by("id")
    today = datetime.today().strftime("%Y-%m-%d")

    context = {
        "todos": todos,
        "today": today,
    }

    return render(request, "todo/index.html", context)
```

- R(READ) + U(UPDATE) : 할 일 수정하기

```py
# completed 여부 수정
def check(request, pk):
    # 1. pk에 해당하는 데이터의 completed
    todo = Todo.objects.get(id=pk)

    # 2. completed 여부(True/False) 수정
    if todo.completed == True:
        todo.completed = False
    else:
        todo.completed = True

    # 3. 수정된 데이터 저장
    todo.save()

    return redirect("todo:index")
```

```py
# 수정할 pk의 할 일 데이터 읽어옴
def edit(request, pk):
    # 1. pk에 해당하는 데이터
    todo = Todo.objects.get(id=pk)
    # 날짜 포멧 맞춤
    deadline = todo.deadline.strftime("%Y-%m-%d")

    context = {
        "todo": todo,
    }

    return render(request, "todo:index", context)
```

```py
# 수정할 pk의 할 일을 새로 입력받은 데이터로 수정
def update(request, pk):
    # 1. pk에 해당하는 데이터
    todo = Todo.objects.get(id=pk)

    # 2. parameter로 날라온 데이터를 받아서
    content = request.GET.get("content")
    priority = int(request.GET.get("priority"))
    deadline = request.GET.get("deadline")

    # 3. 데이터 수정
    todo.content = content
    todo.priority = priority
    todo.deadline = deadline

    # 4. 수정된 데이터 저장
    todo.save()

    return redirect("todo:index")
```

- D(DELETE) : 할 일 삭제하기

```py
def delete(request, pk):
    # pk에 해당하는 글 삭제
    Todo.objects.get(id=pk).delete()
    return redirect("todo:index")
```



### 7. `todo/templates` 설정

- `todo/` 아래 `templates/todo/` 폴더 생성
- `TODO/templates/base.html` 상속 받음

```html
{% extends 'base.html' %}

{% block content %}
	<!-- 내부 작성 -->
{% endblock %}
```

- `todo/templates/todo/` 아래 `index.html` 파일 생성
- 내비게이션 바
  - 브랜드 아이콘 설정 : 부트스트랩 아이콘
  - 홈 : `<a>` 활용, 해당 페이지 상단으로 이동
  - 추가 : `<a>` 활용, 해당 페이지의 할 일 추가하기로 이동
  - 목록 : `<a>` 활용, 해당 페이지의 할 일 목록보기로 이동

```html
<!-- 내비게이션 바 -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
  <div class="container-fluid p-3">
    <a class="navbar-brand" href="#">
      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-calendar4-week"
        viewBox="0 0 16 16">
        <path
          d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM2 2a1 1 0 0 0-1 1v1h14V3a1 1 0 0 0-1-1H2zm13 3H1v9a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V5z" />
        <path
          d="M11 7.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm-3 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm-2 3a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm-3 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z" />
      </svg>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02"
      aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0 fs-3 h-font">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="{% url 'todo:index' %}">홈</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#add">추가</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#list">목록</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

- 할 일 추가하기 : `<form>`
  - 할 일 : `<input type = "text">` 활용
  - 우선순위 : `<select>`, `<option>` 활용
  - 마감기한 : `<input type = "date">` 활용
  - 할 일 추가 버튼 : `<input type = "submit">` 활용

```html
<!-- 할 일 추가하기 -->
<div class="p-3 d-flex flex-column align-items-center bg-primary" id="add">
  <h1 class="m-0 p-3 h-font text-center text-white"><i class="bi bi-plus-square"></i> 할 일 추가</h1>
  <form action="{% url 'todo:create' %}" class="w-100">
    <!-- content -->
    <div class="input-group mb-3">
      <span class="input-group-text" id="content-add">할 일</span>
      <input type="text" name="content" class="form-control" placeholder="할 일을 입력해주세요" aria-describedby="content-add"
        id="content-input">
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
      <input type="date" name="deadline" value="{{ today }}" class="form-control" aria-describedby="deadline-add">
    </div>
    <!-- submit -->
    <input type="submit" value="할 일 추가" class="btn btn-outline-light w-100" id="submit-btn">
  </form>
</div>
```

- 할 일 목록 보기 : `<table>`
  - `<thead>` : 우선순위 / 할 일 / 생성 날짜 / 마감 기한 / 진행 상태 / 상태 변경 / 삭제 를 테이블 헤더로 사용
  - `<tbody>` : id를 기준으로 오름차순으로 정렬한 모든 데이터를 화면에 표시

```html
<!-- 할 일 목록 보기 -->
<div class="p-3 pt-5 d-flex flex-column align-items-center bg-light" id="list">
  <h1 class="m-0 p-3 h-font text-center"><i class="bi bi-check-square"></i> 할 일 목록</h1>
  <table class="table">
    <thead>
      <tr>
        <th scope="col" class="text-center">진행 상태</th>
        <th scope="col" class="text-center">우선순위</th>
        <th scope="col" class="text-center">할 일</th>
        <th scope="col" class="text-center">생성 날짜</th>
        <th scope="col" class="text-center">마감 기한</th>
        <th scope="col" class="text-center">수정</th>
        <th scope="col" class="text-center">삭제</th>
      </tr>
    </thead>
    <tbody class="bg-white">
      {% for todo in todos %}
      {% if todo.completed == True %}
        		<!-- completed 상태가 True일 때 css 설정이 다름 -->
      <tr>
        <td class="text-center">
          <a href="/todo/check/{{ todo.id }}" class="text-black"><i class="bi bi-check-square"></i></a>
        </td>
        <td class="text-center text-decoration-line-through text-secondary">{{ todo.priority }}</td>
        <td class="text-decoration-line-through text-secondary">{{ todo.content }}</td>
        <td class="text-center text-decoration-line-through text-secondary">{{ todo.created_at }}</td>
        <td class="text-center text-decoration-line-through text-secondary">{{ todo.deadline }}</td>
        <td class="text-center">
          <a href="/todo/edit/{{ todo.id }}" class="btn btn-primary btn-sm" data-bs-toggle="modal"
            data-bs-target="#modal{{ todo.pk }}" data-bs-whatever="@mdo"><i class="bi bi-pencil-square"></i></a>
        </td>
        <!-- 할 일 수정하기 -->
        <div class="modal fade" id="modal{{ todo.id }}" tabindex="-1" aria-labelledby="modal{{ todo.id }}Label"
          aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="modal{{ todo.id }}Label"><i class="bi bi-pencil-square"></i> 할 일 수정</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <form action="{% url 'todo:update' todo.id %}" class="w-100">
                  <!-- content -->
                  <div class="input-group mb-3">
                    <span class="input-group-text" id="content-edit">할 일</span>
                    <input type="text" name="content" class="form-control" value="{{ todo.content }}"
                      placeholder="할 일을 입력해주세요" aria-describedby="content-edit" id="content-input">
                  </div>
                  <!-- priority -->
                  <div class="input-group mb-3">
                    <label class="input-group-text" for="priority-edit">우선순위</label>
                    <select class="form-select" name="priority" id="priority-edit">
                      <option value="{{ todo.priority }}" selected hidden>{{ todo.priority }}</option>
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                      <option value="5">5</option>
                    </select>
                  </div>
                  <!-- deadline -->
                  <div class="input-group mb-3">
                    <span class="input-group-text" id="deadline-edit">마감기한</span>
                    <input type="date" name="deadline" value="{{ todo.deadline|date:'Y-m-d' }}" class="form-control"
                      aria-describedby="deadline-edit">
                  </div>
                  <!-- submit -->
                  <input type="submit" value="할 일 수정" class="btn btn-outline-light w-100" id="edit-btn">
                </form>
              </div>
            </div>
          </div>
        </div>
        <!-- 할 일 삭제하기 -->
        <td class="text-center">
          <a href="/todo/delete/{{ todo.id }}" class="btn btn-danger btn-sm"><i class="bi bi-trash3-fill"></i></a>
        </td>
      </tr>
      {% else %}
      			<!-- completed 상태가 False일 때 css 설정이 다름 -->
      {% endif %}
      {% endfor %}
    </tbody>
  </table>
</div>
```

- 상태 변경하기
  - 버튼을 누르면 해당 할 일의 상태(True/False)가 수정됨
  - 부트스트랩 아이콘을 이용해서 상태에 따라 아이콘 변경

```html
<a href="/todo/check/{{ todo.id }}" class="text-black">
    <i class="bi bi-check-square"></i>
</a>
```

- 할 일 수정하기
  - 버튼을 누르면 수정하기로 한 할 일의 id를 넘겨줌
  - 해당 할 일의 데이터를 모달 팝업창으로 보여줌

```html
<a href="/todo/edit/{{ todo.id }}" 
   class="btn btn-primary btn-sm" 
   data-bs-toggle="modal"
   data-bs-target="#modal{{ todo.pk }}" 
   data-bs-whatever="@mdo">
   <i class="bi bi-pencil-square"></i>
</a>
```

```html
<div class="modal fade" id="modal{{ todo.id }}" tabindex="-1" aria-labelledby="modal{{ todo.id }}Label" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="modal{{ todo.id }}Label"><i class="bi bi-pencil-square"></i> 할 일 수정</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
				<form action="{% url 'todo:update' todo.id %}" class="w-100">
                  <!-- content -->
                  <div class="input-group mb-3">
                    <span class="input-group-text" id="content-edit">할 일</span>
                    <input type="text" name="content" class="form-control" value="{{ todo.content }}"
                      placeholder="할 일을 입력해주세요" aria-describedby="content-edit" id="content-input">
                  </div>
                  <!-- priority -->
                  <div class="input-group mb-3">
                    <label class="input-group-text" for="priority-edit">우선순위</label>
                    <select class="form-select" name="priority" id="priority-edit">
                      <option value="{{ todo.priority }}" selected hidden>{{ todo.priority }}</option>
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                      <option value="5">5</option>
                    </select>
                  </div>
                  <!-- deadline -->
                  <div class="input-group mb-3">
                    <span class="input-group-text" id="deadline-edit">마감기한</span>
                    <input type="date" name="deadline" value="{{ todo.deadline|date:'Y-m-d' }}" class="form-control"
                      aria-describedby="deadline-edit">
                  </div>
                  <!-- submit -->
                  <input type="submit" value="할 일 수정" class="btn btn-outline-light w-100" id="edit-btn">
                </form>
			</div>
		</div>
	</div>
</div>
```

- 할 일 삭제하기
  - 버튼을 누르면 해당 할 일이 삭제됨

```html
<a href="/todo/delete/{{ todo.id }}" class="btn btn-danger btn-sm">
    <i class="bi bi-trash3-fill"></i>
</a>
```

