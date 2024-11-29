from rest_framework.permissions import BasePermission

from projects.models import Project
from projects.serializers.common import ProjectSerializer
from projects.service import user_can_change_project

class CanChangeProjectOrStaff(BasePermission):
    SAFE_METHODS = ['GET']
    def has_object_permission(self, request, view, obj):
        if request.method in self.SAFE_METHODS or user_can_change_project(obj,request.user) or request.user.is_staff:
            return True
        return False

class UserInProjectOrStaff(BasePermission):
    SAFE_METHODS = ['GET']

    def has_object_permission(self, request, view, obj):
        project = ProjectSerializer(instance=obj)
        if request.method in self.SAFE_METHODS or (request.user.id in project.data["users"]) or request.user.is_staff:
            return True
        return False