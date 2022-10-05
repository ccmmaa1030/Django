from django.urls import path
from . import views

# app 단위로 URL 설정
app_name = 'articles'

urlpatterns = [
    # http://127.0.0.1:8000/articles/
    path('', views.index, name='index'),
    # http://127.0.0.1:8000/articles/create/
    path('create/', views.create, name='create'),
    # http://127.0.0.1:8000/articles/int:pk/
    path('<int:pk>', views.detail, name='detail'),
    # http://127.0.0.1:8000/articles/int:pk/delete/
    path('<int:pk>/delete/', views.delete, name='delete'),
    # http://127.0.0.1:8000/articles/int:pk/update/
    path('<int:pk>/update/', views.update, name='update'),
]