from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


# 新規登録
class SignupView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('movieee:index.html')
    context = {
      'form': UserCreationForm()
    }
    return render(request, 'movieee/signup.html', context)

  def post(self, request, *args, **kwargs):
    form = UserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      input_username = form.cleaned_data['username']
      input_password = form.cleaned_data['password1']
      new_user = authenticate(username=input_username, password=input_password)
      if new_user is not None:
        login(request, new_user)
        return redirect('movieee:users_detail', pk=new_user.pk)
signup = SignupView.as_view()