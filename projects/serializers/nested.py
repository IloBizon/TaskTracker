from rest_framework import serializers
from projects.models import ProjectUser, Project



class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ["user","role"]


class ProjectPrettySerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField("user_role_serializer")

    def user_role_serializer(self, project):
        from projects.service import get_all_project_roles

        return get_all_project_roles(project)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "creation_date", "last_update", "users", "is_active"]