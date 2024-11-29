from users.models import User
from projects.models import ProjectUser, ProjectHistory
from projects.serializers.nested import ProjectRoleSerializer, ProjectHistoryPrettySerializer


def get_all_roles_in_projects(user: User):
    project_users = ProjectUser.objects.filter(user=user.id)
    if not project_users:
        return []

    if len(project_users) > 1:
        project_role = ProjectRoleSerializer(instance=project_users, many=True)
    else:
        project_role = ProjectRoleSerializer(instance=project_users.first(), many=False)

    return project_role.data

def get_project_history(user: User):
    project_history = ProjectHistory.objects.filter(user=user.id)
    if not project_history:
        return []

    if len(project_history) > 1:
        history = ProjectHistoryPrettySerializer(instance=project_history, many=True)
    else:
        history = ProjectHistoryPrettySerializer(instance=project_history.first(), many=False)

    return history.data

def staff_only(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_staff:
            func(self, request ,*args, **kwargs)
        else:
            self.permission_denied(request)
    return wrapper


