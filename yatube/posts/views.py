from django.conf import settings
from django.shortcuts import render, get_object_or_404


from .models import Post, Group


def index(request):
    posts = Post.objects.all()[:settings.POST_COUNT]
    return render(request, 'posts/index.html', {'posts': posts})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all()[:settings.POST_COUNT]
    return render(
        request,
        'posts/group_list.html',
        {'group': group, 'posts': posts}
    )
