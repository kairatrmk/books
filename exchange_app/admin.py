from django.contrib import admin
from users.models import CustomUser
from exchange_app.serializers import ExchangeCreateSerializer
from django.utils.html import format_html

from .models import Book, BookImage, Exchange, Genre, Status, Condition


class ExchangeAdmin(admin.ModelAdmin):
    list_display = "id", "user_sender", "book_sender", "user_receiver", "book_receiver", "status"

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


class BookImageInline(admin.TabularInline):  # Или admin.StackedInline
    model = BookImage
    extra = 7


class BookAdmin(admin.ModelAdmin):
    inlines = [BookImageInline]
    list_display = ('id', 'user_temp', 'available', 'title', 'author', 'genre', 'condition', 'display_images')

    def display_images(self, obj):
        # Получите изображение книги
        images = obj.images.all()
        if images:
            # Отобразите первое изображение
            return format_html('<img src="{}" width="50" height="50" />', images[0].image.url)
        return "No Image"

    display_images.short_description = 'Images'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Condition, ConditionAdmin)



