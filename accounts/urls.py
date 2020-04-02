from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('users/<str:pk>/', views.users_detail, name='users_detail'),
    path('users/<str:pk>/profile_change/', views.profile_change, name='profile_change'),
    path('password_change/', views.password_change, name='password_change'),
    path('password_change/done/', views.password_change_done, name='password_change_done'),
]