from django.urls import path
from . import views

app_name = 'movieee'
urlpatterns = [
  path('', views.index, name='index'),
]