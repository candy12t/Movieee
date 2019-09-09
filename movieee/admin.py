from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'title','created_date', 'updated_date',)
  list_display_links = ('id', 'title',)

admin.site.register(Post, PostAdmin)