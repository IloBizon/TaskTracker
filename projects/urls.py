from django.urls import path
from . import views

urlpatterns = [
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