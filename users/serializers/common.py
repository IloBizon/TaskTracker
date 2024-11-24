from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)
    class Meta:
        model = User
        fields = ["id","username", "password", "avatar", "first_name", "last_name", "projects"]
