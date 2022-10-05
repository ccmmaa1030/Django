from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.

# view 함수 생성, template/articles 생성 
def index(request):
    # DB에서 게시글 가져옴 + pk의 내림차순으로 정렬
    articles = Article.objects.order_by('-pk')
    # template에 전달
    context = {
        'articles': articles
    }
    # 게시글 목록 페이지로 이동
    return render(request, 'articles/index.html', context)

def create(request):
    # POST 요청 처리
    if request.method == 'POST':
        # ModelForm에서 입력받은 데이터
        article_form = ArticleForm(request.POST)
        # 유효성 검사를 통과하면
        if article_form.is_valid():
            # DB에 저장
            article_form.save()
            # index 페이지 redirect
            return redirect('articles:index')
    # GET 요청 처리
    else: 
        article_form = ArticleForm()
    # template에 전달
    context = {
        'article_form': article_form
    }
    # 게시글 생성 페이지로 이동
    return render(request, 'articles/create.html', context=context)

def detail(request, pk):
    # DB에서 특정 게시글 하나만 가져옴
    article = Article.objects.get(pk=pk)
    # template에 전달
    context = {
        'article': article
    }
	# 게시글 상세보기 페이지로 이동
    return render(request, 'articles/detail.html', context)

def delete(request, pk):
    # DB에서 특정 게시글 하나만 가져옴
    article = Article.objects.get(pk=pk)
    # 게시글 삭제
    article.delete()
	# index 페이지 redirect
    return redirect('articles:index')

def update(request, pk):
    # DB에서 특정 게시글 하나만 가져옴
    article = Article.objects.get(pk=pk)
	# POST 요청 처리
    if request.method == 'POST':
        # POST : input 값 가져와서, 검증하고, DB에 저장
        article_form = ArticleForm(request.POST, instance=article)
        # 유효성 검사를 통과하면
        if article_form.is_valid():
            # DB에 저장
            article_form.save()
            # detail 페이지로 redirect
            return redirect('articles:detail', article.pk)
    # GET 요청 처리
    else:
        # 특정 게시글의 데이터를 form에 입력
        article_form = ArticleForm(instance=article)
    # template에 전달
    context = {
        'article_form': article_form
    }
	# 게시글 수정 페이지로 이동
    return render(request, 'articles/update.html', context)