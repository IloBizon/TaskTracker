from projects.models import Project, ProjectUser
from projects.serializers.nested import UserRoleSerializer
from users.models import User
from users.serializers import UserSerializer



def get_all_project_roles(project: Project):
    user_serializer = UserSerializer(instance=project.users, many=True)

    ids = []
    for user in user_serializer.data:
        ids.append(user["id"])

    roles = ProjectUser.objects.filter(project=project.id).filter(user__in=ids)

    roles_serializer = UserRoleSerializer(instance=roles, many=True)

    return roles_serializer.data


def validate_user(user: User, project: Project) -> bool:
    from projects.serializers.common import ProjectSerializer
    serialized_project = ProjectSerializer(instance=project).data
    serialized_user = UserSerializer(instance=user).data

    if serialized_user["id"] not in serialized_project["users"]:
        return True
    else:
        return False


