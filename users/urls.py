from django.urls import path
from . import views

urlpatterns = [
    path("register", views.RegisterUser.as_view()),
    path("login", views.UserLogin.as_view()),
    path("", views.UserViewSet.as_view({"get": 'list'})),
    path('<int:pk>', views.UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete':'destroy'})),
    path("<int:pk>/profile", views.GetUserProfile.as_view()),

]