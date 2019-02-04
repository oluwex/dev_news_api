from django.contrib import admin

from .models import Article

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'timestamp']


admin.site.register(Article, ArticleAdmin)
