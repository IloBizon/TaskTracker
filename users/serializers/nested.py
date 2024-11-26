from rest_framework import serializers
from users.models import User
from users.service import get_all_roles_in_projects, get_project_history

class UserPrettySerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)
    projects = serializers.SerializerMethodField(method_name="get_projects")
    project_history = serializers.SerializerMethodField("get_project_history")

    def get_projects(self, user):
        roles =  get_all_roles_in_projects(user)

        return roles

    def get_project_history(self, user):
        history = get_project_history(user)

        return history

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "avatar", "projects", "project_history"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "avatar", "first_name", "last_name"]
