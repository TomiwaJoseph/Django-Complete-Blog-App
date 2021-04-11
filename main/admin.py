from django.contrib import admin
from .models import Blog, Category, Comment, NewsLetterList

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status')
    list_filter = ('status', 'created', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category)
admin.site.register(NewsLetterList)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'commenter', 'parent', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('body',)

