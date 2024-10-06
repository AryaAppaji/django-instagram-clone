from .serializers import MessageSerializer
from ..models import Message, User, Chat
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404

class MessageViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):
        chat_id = request.data.get('chat_id')
        chat = Chat.objects.get(pk=chat_id)
        messages = Message.objects.filter(chat=chat)

        return Response(
            data = messages,
            status=status.HTTP_200_OK
        )
    
    def create(self, request):
        sender_id = request.data.get('sender_id')
        receiver_id = request.data.get('receiver_id')

        sender = User.objects.get(pk=sender_id)
        receiver = User.objects.get(pk=receiver_id)

        chat = Chat.objects.filter(sender=sender, receiver=receiver).first()

        if not chat:
            chat = Chat.objects.create(
                sender = sender,
                receiver = receiver,
            )

        message = Message.objects.create(
            chat = chat,
            message = request.data.get('message'),
        )
        
        message.attachement = request.FILES.get('attachment')
        return Response({
            'msg': 'Message Sent Successfully',
        },status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk)

        chat.message = request.data.get('message')
        chat.attachment = request.data.get('attachment')

        try:
            chat.save()
        except Exception as e:
            return Response({
                'msg': str(e),                
            }, status=status.HTTP_417_EXPECTATION_FAILED)

        return Response(None, status=status.HTTP_417_EXPECTATION_FAILED)
    
    def delete(self, request, pk):
        message = get_object_or_404(Message, pk=pk)

        try:
            message.delete()
        except Exception as e:
            return Response({
                'msg': str(e),                
            }, status=status.HTTP_417_EXPECTATION_FAILED)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
