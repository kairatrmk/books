from django.contrib import admin
from users.models import CustomUser, City


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'city', 'display_favorite_books')
    list_filter = ('city',)
    search_fields = ('email', 'first_name', 'last_name', 'city__title')

    # Add a function to display favorite books
    def display_favorite_books(self, obj):
        return ", ".join([book.title for book in obj.favorite_books.all()])
    display_favorite_books.short_description = 'Favorite Books'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(City)
