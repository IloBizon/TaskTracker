
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from projects.serializers.nested import ProjectPrettySerializer
from users.models import User
from projects.models import Project, ProjectUser
from projects.serializers.common import ProjectSerializer, ProjectUserSerializer
from projects.service import get_all_project_roles, validate_user
from rest_framework.exceptions import APIException

class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectPrettySerializer

class AddUser(APIView):
    serializer_class = ProjectUserSerializer
    def post(self,request):
        project = Project.objects.get(id=request.data['project'])
        user = User.objects.get(id=request.data['user'])

        if validate_user(user, project):
            project_user = ProjectUser.objects.create(
                project = project,
                user = user,
                role = request.data['role']
            )
            project_user_serialized = ProjectUserSerializer(instance=project_user)
            return Response(project_user_serialized.data)
        else:
            response = Response(data="User is already exists in this project!", status=403, exception=True)
            return response


class RemoveUser(APIView):
    serializer_class = ProjectUserSerializer
    def post(self, request):
        project_user = ProjectUser.objects.filter(project=request.data['project'], user=request.data['user'])
        if not project_user:
            return Response("User does not exist in this project!")

        project_user.delete()
        return Response("User is successfully removed!")

class ChangeRole(APIView):
    serializer_class = ProjectUserSerializer
    def post(self, request):
        project_user = ProjectUser.objects.filter(project=request.data['project'], user=request.data['user']).first()
        if not project_user:
            return Response("User does not exist in this project!")
        project_user.role = request.data['role']
        project_user.save()
        serialized_project_user = ProjectUserSerializer(instance=project_user)

        return Response(serialized_project_user.data)


class GetAllRoles(APIView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        project = Project.objects.get(id=pk)
        roles = get_all_project_roles(project)

        return Response(roles)





