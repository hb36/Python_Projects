from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'text', 'created_time']
    list_filter = ['created_time', 'name']


admin.site.register(Comment, CommentAdmin)
