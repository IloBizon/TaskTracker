from rest_framework import serializers

from comments.models import Comment, CommentHistory


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

class CommentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentHistory
        fields = "__all__"


    def create(self, **validated_data):
        return CommentHistory.objects.create(**validated_data)