from django.contrib import admin
from users.models import CustomUser
from exchange_app.serializers import ExchangeCreateSerializer

from .models import *


class ExchangeAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Validate the data using the serializer
        serializer = ExchangeCreateSerializer(data={
            'user_sender': obj.user_sender.id,
            'user_receiver': obj.user_receiver.id,
            'book_sender': obj.book_sender.id,
            'book_receiver': obj.book_receiver.id,
            'status': obj.status.id,
        })

        if serializer.is_valid():
            exchange_instance = serializer.save()  # Save the validated data
            obj.id = exchange_instance.id  # Assign the ID from the saved instance to the current instance
            super().save_model(request, obj, form, change)  # Continue with model saving
        else:
            raise ValueError(serializer.errors)


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_temp', 'available', 'title', 'author', 'genre', 'condition', 'description', 'photo')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Status)
admin.site.register(Condition)



