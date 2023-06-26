from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .utils import make_paginator

MAX_POSTS = 10


def index(request):
    """View-функция для рендера главной страницы."""
    template = 'posts/index.html'
    posts = Post.objects.all()
    page_obj = make_paginator(request, posts, MAX_POSTS)
    return render(request, template, context={'page_obj': page_obj})


def group_posts(request, slug):
    """View-функция для рендера постов в конкртеной группе."""
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = make_paginator(request, posts, MAX_POSTS)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """View-функция для рендера профайла пользователя."""
    temmplate = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    count_posts = posts.count()
    page_obj = make_paginator(request, posts, MAX_POSTS)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            author=author,
            user=request.user
        ).exists()
    context = {
        'author': author,
        'count_posts': count_posts,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, temmplate, context)


def post_detail(request, post_id):
    """View-функция для рендера страницы поста."""
    temmplate = 'posts/post_detail.html'
    selected_post = get_object_or_404(
        Post.objects.select_related('group', 'author',),
        pk=post_id
    )
    count_posts = selected_post.author.posts.count()
    comments = selected_post.comments.all()
    form = CommentForm()
    context = {
        'count_posts': count_posts,
        'selected_post': selected_post,
        'comments': comments,
        'form': form,
    }
    return render(request, temmplate, context)


@login_required
def post_create(request):
    """View-функция для рендера страницы создания поста."""
    template = 'posts/post_create.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('posts:profile', username=f'{request.user}')
    return render(request, template, context={'form': form})


@login_required
def post_edit(request, post_id):
    """View-функция для рендера страницы редактирования поста."""
    template = 'posts/post_create.html'
    post_for_edit = get_object_or_404(Post, pk=post_id)
    if post_for_edit.author == request.user:
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post_for_edit
        )
        if request.method == 'POST':
            if form.is_valid():
                updated_post = form.save(commit=False)
                updated_post.author = request.user
                updated_post.save()
                return redirect('posts:post_detail', post_id=f'{post_id}')
    else:
        return redirect('posts:post_detail', post_id=f'{post_id}')
    context = {
        'is_edit': True,
        'form': form,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    """Добавить комментарий в БД и выполнить редирект."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """View-функция для вывода постов авторов,
    на которых user подписан.
    """
    template = 'posts/follow.html'
    posts = Post.objects.filter(author__following__user=request.user)
    page_obj = make_paginator(request, posts, MAX_POSTS)
    return render(request, template, context={'page_obj': page_obj})


@login_required
def profile_follow(request, username):
    """Подписаться на автора и выполнить редиркет."""
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.update_or_create(
            author=author,
            user=request.user
        )
    return redirect('posts:follow_index')


@login_required
def profile_unfollow(request, username):
    """Отписаться от автора и выполнить редиркет."""
    Follow.objects.filter(
        user=request.user,
        author=get_object_or_404(User, username=username)
    ).delete()
    return redirect('posts:follow_index')
