from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post

def index(request):
  posts = Post.objects.all().order_by('-created_date')
  return render(request, 'movieee/index.html', {'posts': posts})


def users(request, pk):
  user = get_object_or_404(User, pk=pk)
  return render(request, 'movieee/users.html', {'user': user})