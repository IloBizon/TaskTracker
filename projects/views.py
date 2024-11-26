from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import OrderingFilter
from projects.serializers.nested import ProjectPrettySerializer, CreateProjectSerializer
from users.models import User
from projects.models import Project, ProjectUser, ProjectHistory
from projects.serializers.common import ProjectUserSerializer, ProjectSerializer
from projects.service import get_all_project_roles, validate_user, user_can_change_project, add_user_to_project, get_project_role

@extend_schema(tags=["Projects"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список проектов",
        ),
    retrieve=extend_schema(
        summary="Получить проект по id"
    ),
    update=extend_schema(
        summary="Изменение существующего проекта",
        ),
    partial_update=extend_schema(
        summary="Частичное изменение проекта"
        ),
    create=extend_schema(
            summary="Создание нового проекта",
        ),
    destroy =extend_schema(
        summary='Удалить проект'
    )
)
class ProjectView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProjectPrettySerializer
    queryset = Project.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['creation_date', 'last_update']

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().list(request, *args, *kwargs)
        else:
            return Response(exception=True, status=401, data="User is not an admin!")

    def update(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        project = Project.objects.get(id=pk)
        if user_can_change_project(project, request.user):
            request.data["last_update"] = datetime.now()
            return super().update(request, *args, *kwargs)
        else:
            return Response(exception=True, status=401, data="User can not change this project!")


    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        project = Project.objects.get(id=pk)
        if user_can_change_project(project, request.user):
            request.data["last_update"] = datetime.now()
            return super().partial_update(request, *args, *kwargs)
        else:
            return Response(exception=True, status=401, data="User can not change this project!")

    def create(self, request, *args, **kwargs):

        project = super().create(request, *args, **kwargs)
        project_model = Project.objects.get(id=project.data["id"])
        add_user_to_project(request.user, project_model, "5")
        serialized_project = ProjectPrettySerializer(instance=project_model)
        return Response(serialized_project.data)

    def destroy(self, request, *args, **kwargs):
        project = Project.objects.filter(id=self.kwargs["pk"]).first()
        if not project:
            return Response(status=204)

        if get_project_role(project, request.user) == 5 or request.user.is_staff:
            # project.is_active = False
            # project.save()
            # serialized_project = ProjectSerializer(instance=project)
            # users = User.objects.filter(id__in=serialized_project.data["users"])
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(exception=True, status=401, data="User can not delete this project!")




@extend_schema(tags=["Projects"])
@extend_schema_view(
    put=extend_schema(
        summary="Добавить пользователя в проект"
    )
)
class AddUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectUserSerializer
    def put(self,request):
        project = Project.objects.get(id=request.data['project'])
        user = User.objects.get(id=request.data['user'])

        if not user_can_change_project(project, request.user):
            return Response(exception=True, status=401, data="User can not change this project!")

        if validate_user(user, project):
            project_user = add_user_to_project(user, project, request.data["role"])

            return Response(project_user)
        else:
            response = Response(data="User is already exists in this project!", status=403, exception=True)
            return response



@extend_schema(tags=["Projects"])
@extend_schema_view(
    put=extend_schema(
        summary="Удаление пользователя из проекта"
    )
)
class RemoveUser(APIView):
    serializer_class = ProjectUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request):
        project_user = ProjectUser.objects.filter(project=request.data['project'], user=request.data['user']).first()
        if not user_can_change_project(project_user.project, request.user):
            return Response(exception=True, status=401, data="User can not change this project!")

        if not project_user:
            return Response("User does not exist in this project!")

        ProjectHistory.objects.create(
            project=project_user.project,
            user=project_user.user,
            date=datetime.now(),
            historical_record="Пользователь удалён из проекта"
        )

        project_user.delete()
        project = Project.objects.get(id=project_user.project)
        project_user.last_update = datetime.now()
        project.last_update = datetime.now()
        project.save()
        return Response("User is successfully removed!")




@extend_schema(tags=["Projects"])
@extend_schema_view(
    patch=extend_schema(
        summary="Изменить роль пользователя"
    )
)
class ChangeRole(APIView):
    serializer_class = ProjectUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        project_user = ProjectUser.objects.filter(project=request.data['project'], user=request.data['user']).first()
        if not user_can_change_project(project_user.project, request.user):
            return Response(exception=True, status=401, data="User can not change this project!")

        if not project_user:
            return Response("User does not exist in this project!")
        project_user.role = request.data['role']
        project_user.save()
        serialized_project_user = ProjectUserSerializer(instance=project_user)

        return Response(serialized_project_user.data)





@extend_schema(tags=["Projects"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить всех участников и их роли"
    )
)
class GetAllRoles(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = None
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        project = Project.objects.get(id=pk)
        roles = get_all_project_roles(project)

        return Response(roles)





