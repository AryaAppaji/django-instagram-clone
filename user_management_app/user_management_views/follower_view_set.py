from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import FollowerSerializer


class FollowerViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["GET"], url_path="followers")
    def follower_users(self, request):
        followers = request.user.followers.all()
        serialized_data = FollowerSerializer(followers, many=True)

        return Response(serialized_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="following")
    def following_users(self, request):
        follows = request.user.following.all()
        serialized_data = FollowerSerializer(follows, many=True)

        return Response(serialized_data.data, status=status.HTTP_200_OK)
