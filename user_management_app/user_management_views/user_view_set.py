from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


class UserViewSet(ViewSet):
    permission_classes = [HasAPIKey]

    def retrieve(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serialized_data = UserSerializer(user)

        return Response(data=serialized_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        User.objects.create_user(
            username=request.data.get("username"),
            email=request.data.get("email"),
            password=request.data.get("password"),
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
        )

        return Response(
            {"msg": "User Created Successfully"}, status=status.HTTP_201_CREATED
        )

    def update(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        user.username = request.data.get("username")
        user.email = request.data.get("email")
        user.first_name = request.data.get("first_name")
        user.last_name = request.data.get("last_name")
        user.password = make_password(request.data.get("password"))

        try:
            user.save()
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)

        return Response({"msg": "User Updated Successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        try:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)

    @action(detail=False, methods=["GET"], url_path="search")
    def search(self, request):
        term = request.query_params.get("term", "")
        users = User.objects.filter(username__icontains=term)

        serializer = UserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
