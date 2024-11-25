from projects.serializers.common import ProjectSerializer
from tasks.models import Task
from tasks.serializers.common import TaskSerializer
from users.models import User


def user_in_task(task: Task, user: User):
    serialized_task = TaskSerializer(instance=task)
    if user.id in serialized_task.data["users"] or user.is_staff:
        return True
    else:
        return False

def user_can_change_task(task: Task, user: User):
    project = task.project
    serialized_project = ProjectSerializer(instance=project)

    if user.id in serialized_project.data["users"] or user.is_staff:
        return True
    else:
        return False

