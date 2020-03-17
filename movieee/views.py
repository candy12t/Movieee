from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .form import PostForm, CommentForm
from .models import Post, Comment
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# 一覧表示
class IndexView(ListView):
    model = Post
    template_name = 'movieee/index.html'
    context_object_name = 'posts'

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
class PostsNewView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'movieee/posts_new.html'
    form_class = PostForm
    success_url = reverse_lazy('movieee:index')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        messages.success(self.request, 'レビューを投稿しました！')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'レビューの投稿に失敗しました！')
        return super().form_valid(form)

posts_new = PostsNewView.as_view()


# 削除
class PostsDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('movieee:index')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'レビューを削除しました')
        return super().delete(request, *args, **kwargs)

posts_delete = PostsDeleteView.as_view()


# 編集
class PostsEditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'movieee/posts_edit.html'
    form_class = PostForm
    
    def get_success_url(self):
        return reverse_lazy('movieee:posts_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'レビューを更新しました！')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'レビューの更新に失敗しました')
        return super().form_invalid(form)

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