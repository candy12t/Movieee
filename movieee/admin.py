from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'text',)
  list_display_links = ('title',)

admin.site.register(Post, PostAdmin)