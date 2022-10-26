# Django 19



## JavaScript 비동기 처리



### 0. 비동기 처리

- 비동기 처리 : 특정 코드의 연산이 끝날 때까지 코드의 실행을 멈추지 않고 다음 코드를 먼저 실행하는 자바스크립트의 특성
- 콜백 함수를 사용해서 특정 연산이 끝났을 때 원하는 동작을 실행시킬 수 있음
- 콜백 지옥을 해결하는 방법으로 Promise를 사용할 수 있음

#### (1) Axios

- 보다 편리한 AJAX 요청이 가능하도록 도와주는 브라우저를 위한 Promise 기반의 클라이언트
- 확장 가능한 인터페이스와 함게 패키지로 사용이 간편한 라이브러리를 제공
  - `Promise` : 비동기 작업을 관리하는 객체로, 미래의 어떤 상황에 대한 결과 값을 나타내는 약속
  - `.then()` : 성공에 대한 약속
    - 각각의 .then() 블록은 서로 다른 promise를 반환
    - `.then(callback)` : 이전 작업이 성공했을 때 수행할 작업을 나타내는 함수로 이전 작업의 성공 결과를 인자로 전달받음
  - `.catch()` : 실패에 대한 약속
    - `.catch(callback)` : .then이 하나라도 실패하면 동작
  - `.finally(callback)` : Promise 객체를 반환하며 결과와 상관없이 무조건 지정된 callback 함수가 실행
- callback Hell

```javascript
work1(function(result1) {
    work2(result1, function(result2) {
        work3(result2, function(result3) {
            console.log('최종 결과: ' + result3)
        })
    })
})
```

- callback Hell -> Promise

```javascript
work1().then(function(result1) {
    return work2(result1)
})
.then(function(result2) {
    return work3(result2)
})
.then(function(result3) {
    console.log('최종결과: ' + result3)
})
.catch(failureCallback)
```

- axios 실습

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
  <button>클릭</button>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <script>
    const body = document.querySelector('body')
    const title = document.createElement('h1')
    title.innerText = 'AJAX'
    body.appendChild(title)

    const button = document.querySelector('button')
    // 버튼을 클릭하면, 함수를 실행
    button.addEventListener('click', function () {
      const URL = 'https://jsonplaceholder.typicode.com/todos/1'
      // axios는 URL로 요청을 보냄
      // 처리가 완료되면 실행시켜주겠다는 promise
      // 성공적이면 then, 실패면 catch
      axios.get(URL)
        .then(response => {
          // 성공해서 받은 응답 객체를 활용한 조작
          const h2 = document.createElement('h2')
          h2.innerText = response.data.title
          body.appendChild(h2)
          const p = document.createElement('p')
          p.innerText = response.data.userId
          body.appendChild(p)
        })
        .catch(err => console.log(`${err}!!!`))
    })
  </script>
</body>

</html>
```



### 1. 비동기 처리 : 좋아요

#### 1-1. Review 모델

##### (1) 모델 수정

```python
class Review(models.Model):
    ...
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
```

##### (2) 마이그레이션 파일 생성

- `reviews/migrations` 폴더에 생성된 파일 확인

```bash
$ python manage.py makemigrations
```

##### (3) DB 반영

```bash
$ python manage.py migrate
```

#### 1-2. URL 설정

- `reviews/urls.py` 파일에 URL 설정

```python
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    ...
    path('<int:review_pk>/like/', views.like, name='like'),
]
```

#### 1-3. View 설정

- `reviews/views.py` 파일에 함수 추가

```python
from django.http import JsonResponse
...
@login_required
def like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
        is_liked = False
    else:
        review.like_users.add(request.user)
        is_liked = True
    context = {
        'isLiked': is_liked,
        'likeCount': review.like_users.count()
    }
    return JsonResponse(context)
```

#### 1-4. html 작성

- `reviews/detail.html` 파일 수정, `javascript` 코드 추가

```html
...
    <div class="w-100 left px-3">
        {% if request.user.is_authenticated %}
          <p class="fs-3 lh-2 m-1 px-3">
            {% if request.user in review.like_users.all %}
              <i id="like-btn" data-review-id="{{ review.pk }}" class="bi bi-heart-fill"></i>
            {% else %}
              <i id="like-btn" data-review-id="{{ review.pk }}" class="bi bi-heart"></i>
            {% endif %}
            <span id="like-count" class="fs-3 lh-2 m-1">{{ review.like_users.count }}</span>
          </p>
          {% if request.user == review.user %}
            <a class="blue click rounded-pill m-1 px-3" href="{% url 'reviews:update' review.pk %}">UPDATE</a>
            <a class="red click rounded-pill m-1 px-3" href="{% url 'reviews:delete' review.pk %}">DELETE</a>
          {% endif %}
        {% else %}
          <p class="fs-3 lh-2 m-1 px-3">
            <i class="bi bi-heart-fill like-heart"></i>
            {{ review.like_users.count }}
          </p>
        {% endif %}
      </div>
    </div>
...
```

```html
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <script>
    const likeBtn = document.querySelector('#like-btn')
    likeBtn.addEventListener('click', function (evnet) {
      console.log(event.target.dataset)
      axios({method: 'get', url: `/reviews/${event.target.dataset.reviewId}/like/`}).then(response => {
        console.log(response)
        console.log(response.data)
        if (response.data.isLiked === true) {
          event
            .target
            .classList
            .add('bi-heart-fill')
          event
            .target
            .classList
            .remove('bi-heart')
        } else {
          event
            .target
            .classList
            .add('bi-heart')
          event
            .target
            .classList
            .remove('bi-heart-fill')
        }
        const likeCount = document.querySelector('#like-count')
        likeCount.innerText = response.data.likeCount
      })
    })
  </script>
```

