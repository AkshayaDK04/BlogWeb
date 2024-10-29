
# admin.py
from django.contrib import admin
from .models import Content, Comment

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'author', 'created_at', 'total_likes')
    list_filter = ('content_type', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
