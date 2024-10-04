from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Post, Comment, User
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CommentForm, PostForm
from django.contrib.auth import logout as auth_logout

from .serializers import PostSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def post_list(request):

    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'GET':
        serializer = PostSerializer(post)

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return Response({'message': 'City deleted successfully'}, status=204)

@cache_page(60)
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_date')
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
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_date')
    comment_count = get_comment_count(post.id)  # Use cached comment count
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
