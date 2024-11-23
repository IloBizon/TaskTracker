from rest_framework import serializers

from projects.models import Project, ProjectUser
from projects.service import get_all_project_roles

class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = "__all__"



class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["id","name","description", "creation_date", "last_update", "users", "is_active"]