from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.db.models import Avg
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


# from django.contrib.auth import get_user_model


class City(models.Model):
    title = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    image = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=40, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)
    favorite_books = models.ManyToManyField('exchange_app.Book', related_name="favorited_by", blank=True)
    groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True,
        help_text= ('The groups this user belongs to.'),
        related_name='custom_users'  # Вот здесь добавляем related_name
    )
    user_permissions = models.ManyToManyField(Permission, verbose_name=('user permissions'), blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='custom_users'  # И здесь тоже
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code

    def calculate_average_rating(self):
        received_ratings = self.received_ratings.all()  # Получаем оценки, которые пользователь получил

        if received_ratings.exists():
            average_rating = received_ratings.aggregate(Avg('rating'))['rating__avg']
            return average_rating
        else:
            return 0.0  # Возвращаем 0, если нет оценок


class Rating(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_ratings')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_ratings')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    exchange_request = models.ForeignKey('exchange_app.Exchange', on_delete=models.CASCADE, related_name='ratings', default=None)

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("Нельзя оценить самого себя.")