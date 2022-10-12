from django.core.paginator import Paginator

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Group, User


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'posts/index.html',
        {'page_obj': page_obj}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'posts/group_list.html',
        {'group': group, 'page_obj': page_obj}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.all().filter(author__username=username)
    count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'posts/profile.html',
        {
            'page_obj': page_obj,
            'author': author,
            'count': count
        }
    )


def post_detail(request, post_id):
    post_text = Post.objects.get(id=post_id)
    counter = Post.objects.filter(author=post_text.author).count()
    return render(
        request,
        'posts/post_detail.html',
        {
            'post_text': post_text,
            'counter': counter,
        }
    )


@login_required
def post_create(request):
    is_edit = False
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    return render(
        request,
        'posts/create_post.html',
        {
            'form': form,
            'is_edit': is_edit
        }
    )


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('posts:post_detail', post.pk)
        context = {'form': form, "is_edit": is_edit}
        return render(request, "posts/create_post.html", context)
