from ..models import Story
from .serializers import StorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class StoryViewSet(ViewSet):
    permission_classes = [HasAPIKey]

    def list(self, request):
        stories = Story.objects.all()
        serialized_data = StorySerializer(stories, many=True)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        story = get_object_or_404(Story, pk=pk)
        serialized_data = StorySerializer(story)

        return Response(data=serialized_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = StorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        story = Story.objects.create(
            user=request.user.id,
        )

        story.attachement = request.FILES.get("attachement")
        return Response(
            {"msg": "User Created Successfully"}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        story = get_object_or_404(Story, pk=pk)

        try:
            story.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)
