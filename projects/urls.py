from django.urls import path, include
from . import views
from tasks import views as tasks_views

urlpatterns = [
    path("tasks/comments/", include("comments.urls")),
    path("<int:pk>/tasks", tasks_views.GetProjectTasks.as_view()),
    path("tasks/", include("tasks.urls")),
    path("", views.ProjectView.as_view({'get': 'list','post': 'create'})),
    path('<int:pk>', views.ProjectView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'})),
    path('add-user', views.AddUser.as_view()),
    path("remove-user", views.RemoveUser.as_view()),
    path("get-roles/<int:pk>/",views.GetAllRoles.as_view()),
    path("change-role", views.ChangeRole.as_view())
]