from rest_framework import serializers

from comments.models import Comment


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment"]
