# Register your practise here.
from .models import Post, Comment
from django.contrib import admin

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time',]
    list_filter = ['create_time',]
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ['title', 'text',]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')