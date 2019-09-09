from django.urls import path
from . import views

app_name = 'movieee'
urlpatterns = [
  path('', views.index, name='index'),
  path('users/<int:pk>', views.users, name='users'),
]