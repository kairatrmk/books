from rest_framework import serializers
from django.contrib.auth import get_user_model

from exchange_app.models import Book
from .models import *

from users.tasks import send_confirmation_email
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'city', 'phone_number', 'email',
                  'image']  # Укажите поля, которые вы хотите разрешить обновлять

    def update(self, instance, validated_data):
        # Проходит по каждому полю в validated_data и обновляет соответствующее поле в instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'phone_number', 'first_name', 'last_name', 'city']

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError("Passwords don't same!")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email(user.email, code)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            msg = 'Не удается выполнить аутентификацию с использованием предоставленных учетных данных'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    favorite_books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'city', 'favorite_books']


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError('Пользователь с таким email не найден.')
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        token = RefreshToken.for_user(user)

        # Создание ссылки для сброса пароля
        reset_url = f"http://your-frontend-url/reset-password/{token}/"  # должна быть действительная ссылка на фронт

        # Отправка email со ссылкой на сброс пароля
        subject = 'Восстановление пароля'
        message = f'Для сброса пароля перейдите по ссылке: {reset_url}'
        user.email_user(subject, message)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['title']


class CustomAnotherUserSerializer(serializers.ModelSerializer):
    city_name = CityDetailSerializer(source='city', read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['image', 'first_name', 'last_name', 'city_name', 'average_rating']

    def get_average_rating(self, obj):
        return obj.calculate_average_rating()


class CustomUserProfileSerializer(CustomAnotherUserSerializer):
    # Добавьте поля для отображения при просмотре своего профиля
    class Meta:
        model = CustomUser
        fields = ['image', 'first_name', 'last_name', 'city_name', 'average_rating', 'email', 'phone_number']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'