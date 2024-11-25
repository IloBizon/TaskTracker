from rest_framework import serializers

from comments.models import Comment


class IdCommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.PrimaryKeyRelatedField(source="id", queryset=Comment.objects.all())
    class Meta:
        model = Comment
        fields = ["comment_id", "comment"]
