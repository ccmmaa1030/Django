from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie
from .forms import MovieForm

# Create your views here.

def index(request):
    # DB에서 영화정보 가져옴 + pk의 내림차순으로 정렬
    movies = Movie.objects.order_by('-pk')
    # template에 전달
    context = {
        'movies': movies
    }
    # index 페이지로 이동
    return render(request, 'movies/index.html', context)

def detail(request, pk):
    # DB에서 특정 영화정보 하나만 가져옴
    movie = Movie.objects.get(pk=pk)
    # template에 전달
    context = {
        'movie': movie
    }
    # detail 페이지로 이동
    return render(request, 'movies/detail.html', context)

@login_required
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

@login_required
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

def delete(request, pk):
    # DB에서 특정 영화정보 하나만 가져옴
    movie = Movie.objects.get(pk=pk)
    # DB 삭제
    movie.delete()
    # index 페이지로 이동
    return redirect('movies:index')