from django.shortcuts import render, get_object_or_404
from apps.blog.models import Post


def blog(request):
    posts = Post.objects.all()
    return render(request, "blogs.html", {"posts": posts})


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    posts = Post.objects.all()[:6].exclude(slug=slug)

    return render(request, "blogs.html", {"post": post, "posts": posts})
