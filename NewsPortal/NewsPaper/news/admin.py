from django.contrib import admin
from .models import Post, Category, Author, Comment, PostCategory
from datetime import datetime


def date_update(modeladmin, request, queryset):
    now = datetime.now()
    queryset.update(post_creation_date=now)
    date_update.short_description = 'Изменение времени публикации'


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'post_creation_date', ]
    list_display_links = ['title', ]
    list_filter = ['author_name', 'post_category']
    search_fields = ('title', 'post_content',)
    actions = [date_update]


# Register your models here.
admin.site.register(Post, NewsAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)