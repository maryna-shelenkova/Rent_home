from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_landlord', 'is_renter', 'role')



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def validate_role(self, value):
        valid_roles = ['landlord', 'renter']
        if value not in valid_roles:
            raise serializers.ValidationError(
                f"Invalid role. Allowed values are: {valid_roles}"
            )
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user






