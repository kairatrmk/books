from django.db import models
from django.db.models import CharField
# from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# from users.models import CustomUser
# User = get_user_model()

class Condition(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name


class Book(models.Model):
    available = models.BooleanField(default=True, verbose_name='В наличии',
                                    help_text='Отметьте, если книга доступна для выдачи')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.ForeignKey('Genre', on_delete=models.PROTECT, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    user = models.ForeignKey('users.CustomUser', related_name="books", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='book_photos/', blank=True, null=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=155, db_index=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус')

    def __str__(self) -> CharField:
        return self.name


class Exchange(models.Model):
    user_sender = models.ForeignKey('users.CustomUser', related_name='user_exchanges', on_delete=models.CASCADE)
    user_receiver = models.ForeignKey('users.CustomUser', related_name='user1_exchanges', on_delete=models.CASCADE)
    book_sender = models.OneToOneField('exchange_app.Book', related_name='book_exchanges', on_delete=models.CASCADE)
    book_receiver = models.OneToOneField('exchange_app.Book', related_name='book1_exchanges', on_delete=models.CASCADE)
    status = models.ForeignKey('exchange_app.Status', related_name='book_status', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user_sender.email}'s exchange for {self.book_sender.title}"
