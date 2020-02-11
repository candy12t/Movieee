from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .form import PostForm, CommentForm
from .models import Post, Comment
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


# 一覧表示
class IndexView(ListView):
    model = Post
    template_name = 'movieee/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        posts = Post.objects.all().order_by('-created_date')
        return posts

index = IndexView.as_view()


# 投稿詳細表示
class PostsDetailView(DetailView):
    model = Post
    template_name = 'movieee/posts_detail.html'

posts_detail = PostsDetailView.as_view()


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
            return redirect('accounts:users_detail', pk=request.user.pk)
posts_new = PostsNewView.as_view()


# 削除
class PostsDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        messages.success(request, "削除しました")
        return redirect('accounts:users_detail', request.user.id)
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
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "編集しました！")
        return redirect('movieee:posts_detail', pk=post.pk)
posts_edit = PostsEditView.as_view()


# コメント追加
class CommentsAddView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        context = {
            'form' : CommentForm()
        }
        return render(request, 'movieee/comments_add.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
        return redirect('movieee:posts_detail', pk=post.pk)
comments_add = CommentsAddView.as_view()