from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import PostForm, CommentForm
from .models import Post, Comment
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


# 一覧表示
class IndexView(View):
  def get(self, request, *args, **kwargs):
    posts = Post.objects.all().order_by('-created_date')
    context = {
      'posts': posts
    }
    return render(request, 'movieee/index.html', context)
index = IndexView.as_view()


# ユーザー詳細表示
class UsersDetailView(View):
  def get(self, request, pk, *args, **kwargs):
    user = get_object_or_404(User, pk=pk)
    posts = user.post_set.all().order_by('-created_date')
    context = {
      'user': user,
      'posts': posts
    }
    return render(request, 'movieee/users_detail.html', context)
users_detail = UsersDetailView.as_view()


# 投稿一覧表示
class PostsDetailView(View):
  def get(self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    context = {
      'post': post
    }
    return render(request, 'movieee/posts_detail.html', context)
posts_detail = PostsDetailView.as_view()


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


# 投稿
class PostsNewView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    context = {
      'form': PostForm()
    }
    return render(request, 'movieee/posts_new.html', context)

  def post(self, request, *args, **kwargs):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.save()
      messages.success(request, "投稿しました！")
      return redirect('movieee:users_detail', pk=request.user.pk)
posts_new = PostsNewView.as_view()


# 削除
class PostsDeleteView(LoginRequiredMixin, View):
  def post(self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, "削除しました")
    return redirect('movieee:users_detail', request.user.id)
posts_delete = PostsDeleteView.as_view()


# 編集
class PostsEditView(LoginRequiredMixin, View):
  def get(self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)
    context = {
      'form': form,
      'post': post
    }
    return render(request, 'movieee/posts_edit.html', context)

  def post(self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.save()
      messages.success(request, "編集しました！")
    return redirect('movieee:posts_detail', pk=post.pk)
posts_edit = PostsEditView.as_view()


@login_required
def comments_add(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = post
      comment.user = request.user
      comment.save()
    return redirect('movieee:posts_detail', pk=post.pk)
  else:
    form = CommentForm()
  return render(request, 'movieee/comments_add.html', {'form': form})