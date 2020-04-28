import os
import uuid

from django.db import models

from accounts.models import CustomUser


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4(), ext)
    return os.path.join('image', filename)


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to=get_file_path, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey('movieee.Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment