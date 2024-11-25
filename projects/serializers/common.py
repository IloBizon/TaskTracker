from rest_framework import serializers

from projects.models import Project, ProjectUser, ProjectHistory
from tasks.serializers.common import TaskSerializer


class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = "__all__"



class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, required=False)
    class Meta:
        model = Project
        fields = ["id","name","description", "creation_date", "last_update", "users", "tasks", "is_active"]


class ProjectHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectHistory
        fields = "__all__"