from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

def index(request):
  posts = Post.objects.all().order_by('-created_date')
  return render(request, 'movieee/index.html', {'posts': posts})


def users_detail(request, pk):
  user = get_object_or_404(User, pk=pk)
  return render(request, 'movieee/users_detail.html', {'user': user})


def signup(request):
  form = UserCreationForm()
  return render(request, 'movieee/signup.html', {'form': form})