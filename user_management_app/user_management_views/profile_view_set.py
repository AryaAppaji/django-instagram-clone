from ..models import Profile
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer
from django.core.files.storage import default_storage


class ProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serialized_data = ProfileSerializer(profile, context={"request": request})

        return Response(data=serialized_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        profile = Profile.objects.create(
            user=request.user,
            date_of_birth=request.data.get("date_of_birth"),
            bio=request.data.get("bio"),
            is_public=request.data.get("is_public", True),
        )

        # Handle profile picture upload to S3
        picture = request.FILES.get("picture")
        if picture:
            file_name = default_storage.save(
                f"profiles/{profile.user.id}/{picture.name}", picture
            )
            profile.picture = file_name
            profile.save()

        return Response(
            {
                "msg": "Profile Created Successfully",
                "picture_url": default_storage.url(profile.picture),
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile, data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        profile.user = request.user
        profile.date_of_birth = request.data.get("date_of_birth")
        profile.bio = request.data.get("bio")
        profile.is_public = request.data.get("is_public", True)

        # Handle profile picture upload to S3 during update
        picture = request.FILES.get("picture")
        if picture:
            file_name = default_storage.save(
                f"profiles/{profile.user.id}/{picture.name}", picture
            )
            profile.picture = file_name

        try:
            profile.save()
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)

        return Response(
            {
                "msg": "Profile Updated Successfully",
                "picture_url": default_storage.url(profile.picture),
            },
            status=status.HTTP_200_OK,
        )
