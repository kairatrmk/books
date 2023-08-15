from django.contrib import admin

# Register your models here.
from django.contrib import admin
from users.models import CustomUser, City


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'city')
    list_filter = ('city',)
    search_fields = ('email', 'first_name', 'last_name', 'city__title')  # Пример поиска по названию города


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(City)

