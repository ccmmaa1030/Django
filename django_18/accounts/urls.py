from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('<int:user_pk>/', views.detail, name='detail'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]