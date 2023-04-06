from django.contrib import admin
from . import models


class TitleAdmin(admin.ModelAdmin):
    fields = ('name', 'year', 'category')
    list_display = ('name', 'year', 'category')
    list_filter = ('year', 'category', 'genre__slug')
    empty_value_display = '-пусто-'
    list_per_page = 20
    search_fields = ('name', )


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'review', 'score', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    fields = ('review', 'author', 'text', 'pub_date')


admin.site.register(models.Title, TitleAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Comment, CommentAdmin)
