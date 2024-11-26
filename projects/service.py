from datetime import datetime

from projects.models import Project, ProjectUser, ProjectHistory
from projects.serializers.common import ProjectUserSerializer
from projects.serializers.nested import UserRoleSerializer
from users.models import User
from users.serializers.common import UserSerializer



def get_all_project_roles(project: Project):
    user_serializer = UserSerializer(instance=project.users, many=True)

    ids = []
    for user in user_serializer.data:
        ids.append(user["id"])

    roles = ProjectUser.objects.filter(project=project.id).filter(user__in=ids)

    roles_serializer = UserRoleSerializer(instance=roles, many=True)

    return roles_serializer.data

def get_project_role(project: Project, user: User) -> int:
    project_user = ProjectUser.objects.filter(project=project, user=user).first()
    if not project_user:
        return 0
    else:
        role = project_user.role
    if role:
        return int(role)
    else:
        return 0

def user_can_change_project(project: Project, user: User) -> bool:
    role = get_project_role(project, user)
    is_staff = user.is_staff

    if is_staff or role >= 3:
        return True
    else:
        return False


def validate_user(user: User, project: Project) -> bool:
    from projects.serializers.common import ProjectSerializer
    serialized_project = ProjectSerializer(instance=project).data
    serialized_user = UserSerializer(instance=user).data

    if serialized_user["id"] not in serialized_project["users"]:
        return True
    else:
        return False

def add_user_to_project(user: User, project: Project, role: str):
    project_user = ProjectUser.objects.create(
        project=project,
        user=user,
        role=str(role)
    )

    project_user_serialized = ProjectUserSerializer(instance=project_user)

    ProjectHistory.objects.create(
        project=project,
        user=user,
        date=datetime.now(),
        historical_record="Пользователь добавлен в проект"
    )
    project.last_update = datetime.now()
    project.save()

    return project_user_serialized.data

