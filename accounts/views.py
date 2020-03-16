from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView, TemplateView
from django.views.decorators.cache import never_cache

from .forms import SignupForm
from .models import CustomUser


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
class SignupView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:index')

    def form_valid(self, form):
        messages.success(self.request, '新規登録完了しました！')
        return super().form_valid(form)


signup = SignupView.as_view()


# ユーザー詳細表示
class UsersDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=pk)
        posts = user.post_set.all().order_by('-created_date')
        context = {
            'user': user,
            'posts': posts
        }
        return render(request, 'accounts/users_detail.html', context)


users_detail = UsersDetailView.as_view()