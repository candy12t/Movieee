from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# 新規登録
class SignupView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('movieee:index')
    context = {
      'form': UserCreationForm()
    }
    return render(request, 'accounts/signup.html', context)

  def post(self, request, *args, **kwargs):
    form = UserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      input_username = form.cleaned_data['username']
      input_password = form.cleaned_data['password1']
      new_user = authenticate(username=input_username, password=input_password)
      if new_user is not None:
        login(request, new_user)
        return redirect('accounts:users_detail', pk=new_user.pk)
signup = SignupView.as_view()


# ユーザー詳細表示
class UsersDetailView(View):
  def get(self, request, pk, *args, **kwargs):
    user = get_object_or_404(User, pk=pk)
    posts = user.post_set.all().order_by('-created_date')
    context = {
      'user': user,
      'posts': posts
    }
    return render(request, 'accounts/users_detail.html', context)
users_detail = UsersDetailView.as_view()