from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from users.serializers.common import UserSerializer, UserLoginSerializer
from .serializers.nested import UserPrettySerializer, UserRegisterSerializer
from users.service import staff_only


@extend_schema(tags=["Users"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех пользователей",
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    @staff_only
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, *kwargs)

    @staff_only
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, *kwargs)

    @staff_only
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, *kwargs)

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs["pk"])
        if request.user.is_staff or request.user.id == self.kwargs["pk"]:
            user.is_active = False
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            self.permission_denied(request)



@extend_schema(tags=["Users"])
@extend_schema_view(
    post=extend_schema(
        summary="Регистрация нового пользователя"
    )
)
class RegisterUser(APIView):
    serializer_class = UserRegisterSerializer
    def post(self,request: Request):
        if request.data['avatar']:
            user = User.objects.create_user(request.data['username'],request.data['password'],request.data['first_name'],request.data['last_name'], avatar=request.data['avatar'])
        else:
            user = User.objects.create_user(request.data['username'], request.data['password'], request.data['first_name'], request.data['last_name'])

        token = RefreshToken.for_user(user)

        return Response({
        'refresh': str(token),
        'access': str(token.access_token),
        }
)


@extend_schema(tags=["Users"])
@extend_schema_view(
    post=extend_schema(
        summary="Логин пользователя"
    )
)
class UserLogin(APIView):
    serializer_class=UserLoginSerializer
    def post(self, request):

        user = User.objects.filter(username=request.data["username"]).first()

        if not user or not user.check_password(request.data["password"]):
            self.permission_denied(request, message="Username or password is incorrect", code=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })





@extend_schema(tags=["Users"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить профиль пользователя"
    )
)
class GetUserProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,  *args, **kwargs):
        pk = self.kwargs['pk']
        user = User.objects.get(id=pk)

        return Response(UserPrettySerializer(instance=user).data)


