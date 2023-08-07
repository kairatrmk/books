from django.contrib import admin

from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('available', 'title', 'author', 'genr', 'condition', 'description', 'user', 'photo')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

# class BookExcangeAdmin(admin.ModelAdmin):
#     list_display = ('requester', 'receiver', 'book_offered', 'book_requested', 'status', 'created_at')

# Register your models here
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Status)
admin.site.register(Exchange)
# admin.site.register(ExchangeRequest)


