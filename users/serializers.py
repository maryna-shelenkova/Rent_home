from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User



class UserSerializer(serializers.ModelSerializer):
    # Сериализатор для модели пользователя
    class Meta:
        model = User
        # Поля, которые будут возвращаться в ответе
        fields = ('id', 'username', 'email', 'is_landlord', 'is_renter', 'role')



class UserRegistrationSerializer(serializers.ModelSerializer):
    # Поле для пароля, будет записываться, но не возвращаться клиенту
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # Повтор пароля для проверки совпадения
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # Используем только нужные поля: username, email, password, password2 и role
        fields = ('username', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        # Проверяем совпадение паролей
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        # Удаляем password2, он нам не нужен при создании пользователя
        validated_data.pop('password2')
        # Создаём пользователя с указанными username, email и ролью
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        # Устанавливаем пароль (хэшируется)
        user.set_password(validated_data['password'])
        user.save()
        return user





