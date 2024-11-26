from rest_framework import serializers

from comments.serializers.common import CommentHistorySerializer
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    comment_history = CommentHistorySerializer(many=True, required=False)
    class Meta:
        model = Task
        fields = ["id", "name", "description", "project", "users", "status", "priority", "creation_date", "due_date",
                  "testing_responsible", "comments", "comment_history"]


