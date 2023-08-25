from django.contrib.auth.models import User
from rest_framework import serializers

from users.serializers import RatingSerializer
from .models import Exchange, Book, Genre
from users.models import Rating


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'
#         read_only_fields = ('user',)  # Поля, которые можно только читать
#
#     def create(self, validated_data):
#         # Добавляем текущего пользователя как владельца книги
#         validated_data['user'] = self.context['request'].user
#         return super().create(validated_data)


class BookExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('user', 'available')  # Поля, которые можно только читать
        content_type = 'application/json'

    def create(self, validated_data):
        # Добавляем текущего пользователя как владельца книги
        validated_data['user_temp'] = self.context['request'].user
        validated_data['available'] = True
        return super().create(validated_data)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GenreAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class BookAllSerializer(serializers.ModelSerializer):
    genre = GenreAllSerializer()  # Используем сериализатор GenreSerializer для поля genre

    class Meta:
        model = Book
        fields = ['photo', 'title', 'author', 'genre']


from rest_framework import serializers
from .models import Exchange, Book


class ExchangeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'

    def validate(self, data):
        user_sender = data['user_sender']
        book_sender = data['book_sender']

        # Check if the book_sender belongs to the user_sender
        if not Book.objects.filter(id=book_sender.id, user_temp=user_sender).exists():
            raise serializers.ValidationError("Invalid book_sender ID or book not owned by user_sender.")

        return data


class ExchangeSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Exchange
        fields = '__all__'


class ExchangeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ['user_sender_rating', 'user_receiver_rating']


