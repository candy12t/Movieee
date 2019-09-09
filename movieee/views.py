from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def index(request):
  return render(request, 'movieee/index.html')


def users(request, pk):
  user = get_object_or_404(User, pk=pk)
  return render(request, 'movieee/users.html', {'user': user})