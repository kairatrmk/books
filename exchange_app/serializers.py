from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book

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
    



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('user',)  # Поля, которые можно только читать

    def create(self, validated_data):
        # Добавляем текущего пользователя как владельца книги
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
