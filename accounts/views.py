from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views.decorators.cache import never_cache


class IndexView(TemplateView):
    template_name = 'accounts/index.html'
index = IndexView.as_view()


# カスタムログイン
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        messages.success(self.request, 'ログインしました！')
        return HttpResponseRedirect(self.get_success_url())


login = CustomLoginView.as_view()


# カスタムログアウト
class CustomLogoutView(LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        auth_logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            messages.success(self.request, 'ログアウトしました！')
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)


logout = CustomLogoutView.as_view()


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