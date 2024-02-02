from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk",
                  "last_login",
                  "username",
                  "email",
                  "is_active",
                  "experience",
                  "balance")
