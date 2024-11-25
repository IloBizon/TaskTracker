from rest_framework import serializers

from tasks.models import Task
from users.models import User


class UserTask(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    class Meta:
        model = Task
        fields = ["user", "task"]
