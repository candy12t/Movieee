from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'movieee'
urlpatterns = [
  path('', views.index, name='index'),
  # path('users/<int:pk>/', views.users_detail, name='users_detail'),
  # path('login/', auth_views.LoginView.as_view(template_name='movieee/login.html'), name='login'),
  # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('posts/new/', views.posts_new, name='posts_new'),
  path('posts/<int:pk>/', views.posts_detail, name='posts_detail'),
  path('posts/<int:pk>/edit/', views.posts_edit, name='posts_edit'),
  path('posts/<int:pk>/delete/', views.posts_delete, name='posts_delete'),
  path('posts/<int:pk>/comments_add/', views.comments_add, name='comments_add'),
]