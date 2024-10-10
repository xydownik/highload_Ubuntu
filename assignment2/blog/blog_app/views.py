from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.cache import cache_page
from rest_framework.generics import get_object_or_404

from .models import Post, Comment
from django.shortcuts import render, redirect
from .forms import CommentForm, PostForm


# Create your views here.

@cache_page(60)
def post_list_view(request):
    posts =   Post.objects.prefetch_related('comments').all().order_by('-created_date')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


def get_comment_count(post_id):
    cache_key = f'post_{post_id}_comment_count'
    count = cache.get(cache_key)
    if count is None:
        count = Comment.objects.filter(post_id=post_id).count()
        cache.set(cache_key, count, timeout=60)
    return count


def post_detail_view(request, id):
    post = get_object_or_404(Post.objects.prefetch_related('comments'), id=id)
    comments = post.comments.all().order_by('-created_date')
    comment_count = get_comment_count(post.id)
    # comment_count = post.comments.count()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()


    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_count': comment_count,
        'form': form
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/delete_post.html', {'post': post})


def health_check(request):
    return JsonResponse({'status': 'ok'})