from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from rest_framework.generics import get_object_or_404

from forms import CommentForm
from models import Post, Comment


# Create your views here.

@cache_page(60)
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')

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
        'form': form
    })


def get_comment_count(post_id):
    cache_key = f'post_{post_id}_comment_count'
    count = cache.get(cache_key)
    if count is None:
        count = Comment.objects.filter(post_id=post_id).count()
        cache.set(cache_key, count, timeout=300)  # Cache for 5 minutes
    return count


def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')
    comment_count = get_comment_count(post.id)  # Use cached comment count

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            # Invalidate cache for comment count
            cache.delete(f'post_{post.id}_comment_count')

            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_count': comment_count,
        'form': form
    })