from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .form import PostForm
from .models import Post

def index(request):
  posts = Post.objects.all().order_by('-created_date')
  return render(request, 'movieee/index.html', {'posts': posts})


def users_detail(request, pk):
  user = get_object_or_404(User, pk=pk)
  posts = user.post_set.all().order_by('-created_date')
  return render(request, 'movieee/users_detail.html', {'user': user, 'posts': posts})


def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      input_username = form.cleaned_data['username']
      input_password = form.cleaned_data['password1']
      # フォームの入力値が認証できればユーザーオブジェクト、できなければNoneを返す
      new_user = authenticate(username=input_username, password=input_password)
      if new_user is not None:
        login(request, new_user)
        return redirect('movieee:users_detail', pk=new_user.pk)
  else:
    form = UserCreationForm()
  return render(request, 'movieee/signup.html', {'form': form})


@login_required
def posts_new(request):
  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.save()
      messages.success(request, "投稿しました！")
    return redirect('movieee:users_detail', pk=request.user.pk)
  else:
    form = PostForm()
  return render(request, 'movieee/posts_new.html', {'form': form})


def posts_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'movieee/posts_detail.html', {'post': post})


@require_POST
def posts_delete(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.delete()
  messages.success(request, "削除しました")
  return redirect('movieee:users_detail', request.user.id)


@login_required
def posts_edit(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == 'POST':
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.save()
    return redirect('movieee:index')
  else:
    form = PostForm(instance=post)
  return render(request, 'movieee/posts_edit.html', {'form': form, 'post': post})