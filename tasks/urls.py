from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskView.as_view({"get":"list","post": "create"})),
    path('<int:pk>', views.TaskView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete':'destroy'})),
    path("add-user", views.AddUserToTask.as_view()),
    path("remove-user", views.RemoveUserFromTask.as_view())
]