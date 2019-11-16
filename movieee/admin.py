from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'title','created_date', 'updated_date',)
  list_display_links = ('id', 'title',)


class CommentAdmin(admin.ModelAdmin):
  list_display = ('id', 'comment','created_date',)
  list_display_links = ('id', 'comment',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)