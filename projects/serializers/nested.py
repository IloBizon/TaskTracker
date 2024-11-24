from rest_framework import serializers
from projects.models import ProjectUser, Project, ProjectHistory

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)

class UserRoleSerializer(serializers.ModelSerializer):
    role = ChoiceField(choices=ProjectUser.ROLE_CHOICES)
    class Meta:
        model = ProjectUser
        fields = ["user","role"]

class ProjectRoleSerializer(serializers.ModelSerializer):
    role = ChoiceField(choices=ProjectUser.ROLE_CHOICES)
    class Meta:
        model = ProjectUser
        fields = ["project","role"]


class ProjectPrettySerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField("get_user_roles")

    def get_user_roles(self, project):
        from projects.service import get_all_project_roles

        return get_all_project_roles(project)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "creation_date", "last_update", "users", "is_active"]

class ProjectHistoryPrettySerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="project.name")
    class Meta:
        model = ProjectHistory
        fields = ["project", "historical_record", "date"]

