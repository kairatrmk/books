from django.contrib import admin
from users.models import CustomUser

from .models import *


class ExchangeAdmin(admin.ModelAdmin):
    raw_id_fields = ('user_sender', 'user_receiver')
    list_display = ('id', 'user_sender', 'user_receiver', 'book_sender', 'book_receiver', 'status')



class BookAdmin(admin.ModelAdmin):
    list_display = ('available', 'title', 'author', 'genre', 'condition', 'description', 'user', 'photo')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Status)
admin.site.register(Condition)



