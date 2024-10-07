from .serializers import ChatSerializer
from ..models import Chat
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status


class ChatViewSet(ViewSet):
    permission_classes = [HasAPIKey]

    def list(self, request):
        user = request.user
        sent_chats = user.sent_chats.all()
        received_chats = user.received_chats.all()

        sent_chat = ChatSerializer(sent_chats, many=True)
        received_chat = ChatSerializer(received_chats, many=True)

        return Response(
            {
                "sent_chats": sent_chat.data,
                "received_chats": received_chat.data,
            },
            status.HTTP_200_OK,
        )

    def retrieve(self, request, pk):
        chat = Chat.objects.prefetch_related("messages").get(pk=pk)

        serialized_data = ChatSerializer(chat, many=False)

        return Response(serialized_data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        chat = Chat.objects.prefetch_related("messages").get(pk=pk)

        try:
            chat.delete()
        except Exception as e:
            return Response(str(e), status=status.HTTP_417_EXPECTATION_FAILED)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
