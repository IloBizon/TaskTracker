from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from projects.models import Project
from projects.serializers.common import ProjectSerializer
from projects.service import user_can_change_project
from tasks.filters import TaskFilter
from tasks.models import Task
from tasks.permissions import UserInTaskOrStaff
from tasks.serializers.common import TaskSerializer
from tasks.serializers.nested import UserTask
from tasks.service import user_in_task, user_can_change_task
from users.models import User


@extend_schema(tags=["Tasks"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех задач",
    ),
    retrieve=extend_schema(
        summary="Получить задачу по id"
    ),
    update=extend_schema(
        summary="Изменение существующей задачи",
    ),
    partial_update=extend_schema(
        summary="Частичное изменение задачи"
    ),
    create=extend_schema(
        summary="Создание новой задачи",
    ),
    destroy=extend_schema(
        summary="Удаление задачи",
    )
)
class TaskView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = TaskFilter
    ordering_fields = ("creation_date", "name")

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, *kwargs)
        else:
            return Response(exception=True, status=401, data="User is not an admin!")

    def retrieve(self, request, *args, **kwargs):
        task = Task.objects.get(id=self.kwargs["pk"])

        if user_in_task(task, request.user) or user_can_change_project(task.project, request.user):
            return super().retrieve(request, args, kwargs)
        else:
            self.permission_denied(request)

    def update(self, request, *args, **kwargs):
        task = Task.objects.get(id=self.kwargs["pk"])

        if user_in_task(task, request.user) or user_can_change_project(task.project, request.user):
            return super().update(request, args, kwargs)
        else:
            self.permission_denied(request)

    def partial_update(self, request, *args, **kwargs):
        task = Task.objects.get(id=self.kwargs["pk"])
        if request.data["project"] != task.project.id:
            self.permission_denied(request)
        if user_in_task(task, request.user) or user_can_change_project(task.project,
                                                                       request.user) or request.user.is_staff:
            return super().partial_update(request, *args, **kwargs)
        else:
            self.permission_denied(request)

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=request.data['project'])
        serialized_project = ProjectSerializer(instance=project, many=False)

        if request.user.id in serialized_project.data["users"] or request.user.is_staff:
            task = super().create(request, *args, **kwargs)

            project.tasks.add(task.data["id"])
            if "users" in request.data:
                users = User.objects.filter(id__in=request.data["users"])
                for user in users:
                    user.tasks.add(task.data["id"])

            return task
        else:
            self.permission_denied(request)

    def destroy(self, request, *args, **kwargs):
        task = Task.objects.get(id=self.kwargs["pk"])
        serialized_task = TaskSerializer(instance=task)
        if user_in_task(task, request.user) or user_can_change_project(task.project, request.user):
            for user in serialized_task.data["users"]:
                user.tasks.remove(task)
            project = Project.objects.get(id=task.project.id)
            project.tasks.remove(task)
            return super().destroy(request, args, kwargs)
        else:
            self.permission_denied(request)


@extend_schema(tags=["Tasks"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить задачи проекта"
    )
)
class GetProjectTasks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        tasks = Task.objects.filter(project=pk)

        if len(tasks) > 1:
            serialized_tasks = TaskSerializer(instance=tasks, many=True)
        else:
            serialized_tasks = TaskSerializer(instance=tasks.first(), many=False)

        return Response(serialized_tasks.data)


@extend_schema(tags=["Tasks"])
@extend_schema_view(
    patch=extend_schema(
        summary="Добавить пользователя в задачу"
    )
)
class AddUserToTask(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserTask

    def patch(self, request):
        task = Task.objects.get(id=request.data["task"])
        project = task.project
        serialized_project = ProjectSerializer(instance=project)

        if request.data["user"] in serialized_project.data["users"] and user_can_change_task(task, request.user):
            user = User.objects.get(id=request.data["user"])
            task.users.add(request.data["user"])
            user.tasks.add(task)
            serialized_task = TaskSerializer(instance=task)
            return Response(serialized_task.data)
        else:
            self.permission_denied(request)


@extend_schema(tags=["Tasks"])
@extend_schema_view(
    patch=extend_schema(
        summary="Удалить пользователя из задачи"
    )
)
class RemoveUserFromTask(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, UserInTaskOrStaff]
    serializer_class = UserTask

    def patch(self, request):
        task = Task.objects.get(id=request.data["task"])
        project = task.project
        serialized_project = ProjectSerializer(instance=project)
        user = User.objects.get(id=request.data["user"])
        self.check_object_permissions(request, task)

        if request.data["user"] in serialized_project.data["users"] and user_can_change_task(task, request.user):

            task.users.remove(user)
            user.tasks.remove(task)
            serialized_task = TaskSerializer(instance=task)
            return Response(serialized_task.data)
        else:
            self.permission_denied(request)
