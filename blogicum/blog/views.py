from django.shortcuts import render
from .models import Post, Category
from datetime import datetime
from django.db.models import Q 
from django.http import HttpResponse


# Create your views here.
def index(request):
    template = 'blog/index.html'
    posts_list = Post.objects.all().filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-created_at')[:5]
    context = {'post_list': posts_list}
    print(posts_list)
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    try:
        post = Post.objects.get(pk=pk)
        unpub_posts = Post.objects.filter(
            Q(pub_date__gt=datetime.now()) | Q(
                is_published=False
            ) | Q(
                category__is_published=False
            )
        )
        if (post in unpub_posts):
            return HttpResponse("Страница не найдена", status=404)
        context = {'post': post}
        return render(request, template, context)
    except Post.DoesNotExist:
        return HttpResponse("Страница не найдена", status=404)


def category_posts(request, category_slug):
    cat = Category.objects.get(slug=category_slug)
    if (cat.is_published is False):
        return HttpResponse("Страница не найдена", status=404)
    template = 'blog/category.html'
    posts_list = Post.objects.all().filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__slug=category_slug
    ).order_by('-created_at')
    context = {'category': category_slug, 'post_list': posts_list}
    return render(request, template, context)
