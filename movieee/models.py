from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
  title = models.CharField(max_length=100)
  text = models.TextField()
  image = models.ImageField(upload_to='image')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title