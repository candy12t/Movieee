from django.contrib import admin
from .models import Post, Comment
from django.utils.safestring import mark_safe


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'created_date', 'updated_date',)
    list_filter = ('created_date',)
    search_fields = ('title', 'text',)
    inlines = [CommentInline]

    def image_preview(self, Post):
        if Post.image:
            return mark_safe('<img src="{}" style="width:100px; height:auto;">'.format(Post.image.url))
        else:
            return None

    image_preview.short_description = 'プレビュー'

admin.site.register(Post, PostAdmin)