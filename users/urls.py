from django.urls import path
from . import views

urlpatterns = [
    path("register", views.CreateUser.as_view()),
    path("", views.UserViewSet.as_view({"get": 'list'})),
    path('<int:pk>', views.UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
]