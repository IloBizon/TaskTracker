from datetime import datetime

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from comments.models import Comment, CommentHistory
from comments.serializers.common import CommentSerializer
from comments.serializers.nested import UpdateCommentSerializer
from projects.models import Project
from projects.permissions import UserInProjectOrStaff
from tasks.models import Task


@extend_schema(tags=["Comments"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех комментариев",
    ),
    retrieve=extend_schema(
        summary="Получить комментарий по id"
    ),
    create=extend_schema(
        summary="Создание нового комментария",
    ),
    destroy=extend_schema(
        summary="Удаление комментария",
    )
)
class CommentView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, UserInProjectOrStaff]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, **kwargs)
        else:
            self.permission_denied(request)

    def create(self, request, *args, **kwargs):
        task = Task.objects.get(id=request.data["task"])
        project = Project.objects.get(id=task.project.id)
        self.check_object_permissions(request, project)

        request.data["author"] = request.user.id
        comment = super().create(request, *args, **kwargs)
        task.comments.add(comment.data["id"])

        comment_model = Comment.objects.get(id=comment.data["id"])
        history = CommentHistory.objects.create(
            comment_id=comment_model,
            comment=comment.data["comment"],
            author=comment_model.author,
            date=datetime.now(),
            historical_record="Написан комментарий"
        )
        task.comment_history.add(history)

        request.user.comments.add(comment.data["id"])
        return comment

    def destroy(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=self.kwargs["pk"])
        if comment.author.id == request.user.id or request.user.is_staff:
            comment.task.comments.remove(comment.id)
            request.user.comments.remove(comment.id)

            history = CommentHistory.objects.create(
                comment_id=comment,
                comment=comment.comment,
                author=comment.author,
                date=datetime.now(),
                historical_record="Комментарий удалён"
            )
            comment.task.comment_history.add(history)
            return super().destroy(request, *args, **kwargs)
        else:
            return self.permission_denied(request)


@extend_schema(tags=["Comments"])
@extend_schema_view(
    patch=extend_schema(
        summary="Изменить комментарий",
    ),
)
class UpdateComment(APIView):
    serializer_class = UpdateCommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=self.kwargs["pk"])
        if comment.author.id == request.user.id or request.user.is_staff:
            comment.comment = request.data["comment"]

            history = CommentHistory.objects.create(
                comment_id=comment,
                comment=comment.comment,
                author=comment.author,
                date=datetime.now(),
                historical_record="Комментарий изменён"
            )
            comment.task.comment_history.add(history)
            comment.save()
            serialized_comment = CommentSerializer(instance=comment)
            return Response(serialized_comment.data)
        else:
            self.permission_denied(request)
