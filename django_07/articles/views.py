from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.

# view 함수 생성, template/articles 생성 
def index(request):
    # DB에서 게시글 가져옴
    articles = Article.ojects.order_by('-pk')

    # template에 전달
    context = {
        'articles': articles
    }

    return render(request, 'articles/index.html', context)

# def new(request):
#     article_form = ArticleForm()
#     context = {
#         'article_form': article_form
#     }
#     return render(request, 'articles/new.html', context=context)

def create(request):
    # HTML Form에서 입력받은 데이터
    # 1. method="GET"
    # title = request.GET.get('title')
    # content = request.GET.get('content')
    # 2. method="POST"
    # title = request.POST.get('title')
    # content = request.POST.get('content')
    # DB에 저장
    # Article.objects.create(title=title, content=content)

    # method="POST"이면
    if request.method == 'POST':
        # ModelForm에서 입력받은 데이터
        article_form = ArticleForm(request.POST)
        # 유효성 검사를 통과하면
        if article_form.is_valid():
            # DB에 저장
            article_form.save()
            # index 페이지로 redirect
            return redirect('articles:index')
    else: 
        article_form = ArticleForm()

    # template에 전달
    context = {
        'article_form': article_form
    }

    return render(request, 'articles/new.html', context=context)

def detail(request, pk):
    # 특정 게시글
    article = Article.objects.get(pk=pk)

    # template에 전달
    context = {
        'article': article
    }

    return render(request, 'articles/detail.html', context)

def detail(request, pk):
    # 특정 게시글
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        # POST : input 값 가져와서, 검증하고, DB에 저장
        article_form = ArticleForm(request.POST, instance=article)
        # 유효성 검사를 통과하면
        if article_form.is_valid():
            # DB에 저장
            article_form.save()
            # detail 페이지로 redirect
            return redirect('articles:detail', article.pk)
        # 유효성 검사 통과하지 않으면 => context 부터해서 오류메시지 담긴 article_form을 랜더링
    else:
        # GET : Form을 제공
        # 특정 게시글의 데이터를 form에 입력
        article_form = ArticleForm(instance=article)

    # template에 전달
    context = {
        'article_form': article_form
    }
    
    return render(request, 'articles/update.html', context)