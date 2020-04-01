from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView, TemplateView
from django.views.decorators.cache import never_cache

from .forms import SignupForm
from .models import CustomUser


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
    success_url = reverse_lazy('accounts:login')

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


# パスワード変更
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')


password_change = CustomPasswordChangeView.as_view()


# パスワード変更完了
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        messages.success(self.request, 'パスワード変更完了！')
        return super().dispatch(*args, **kwargs)


password_change_done = CustomPasswordChangeDoneView.as_view()
