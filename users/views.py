from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer

@extend_schema(tags=["Users"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список пользователей",
        ),
    retrieve=extend_schema(
        summary="Получить пользователя по id"
    ),
    update=extend_schema(
        summary="Изменение существующего пользователя",
        ),
    partial_update=extend_schema(
        summary="Частичное изменение пользователя"
        ),
    destroy =extend_schema(
        summary='Удалить пользователя'
    )
)
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()



@extend_schema(tags=["Users"])
@extend_schema_view(
    post=extend_schema(
        summary="Регистрация нового пользователя"
    )
)
class CreateUser(APIView):
    serializer_class = UserSerializer
    def post(self,request: Request):

        if request.data['avatar']:
            user = User.objects.create_user(request.data['username'],request.data['password'],request.data['first_name'],request.data['last_name'], avatar=request.data['avatar'])
        else:
            user = User.objects.create_user(request.data['username'], request.data['password'], request.data['first_name'], request.data['last_name'])

        serializer = UserSerializer(instance=user)

        return Response(serializer.data)