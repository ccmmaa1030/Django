from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review

@login_required
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:index')
    else:
        form = ReviewForm()
    context = {
        'form': form
    }
    return render(request, 'reviews/create.html', context=context)

def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/index.html', context)

def detail(request, pk):
    review = Review.objects.get(pk=pk)
    context = {
        'review': review
    }
    return render(request, 'reviews/detail.html', context)

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:detail', review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form
    }
    return render(request, 'reviews/update.html', context=context)

@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect('reviews:index')