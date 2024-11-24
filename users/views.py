from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer

@extend_schema(tags=["Users"])
@extend_schema_view(
    post=extend_schema(
        summary="Регистрация нового пользователя"
    )
)
class CreateUser(APIView):
    serializer_class = UserSerializer
    def post(self,request: Request):

        user = User.objects.create_user(request.data['username'],request.data['password'],request.data['first_name'],request.data['last_name'])
        serializer = UserSerializer(instance=user)

        return Response(serializer.data)



@extend_schema(tags=["Users"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить всех пользователей"
    )
)
class GetUsers(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(instance=queryset, many=True)
        return Response(serializer.data)