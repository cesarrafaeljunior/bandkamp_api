from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name", "is_superuser"]
        extra_kwargs = {'password': {'write_only': True}, "email": {"required": True, "validators": [UniqueValidator(queryset=User.objects.all())]}}

    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.get("password")
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.set_password(password)

        instance.save()

        return instance
