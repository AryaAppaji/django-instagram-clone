from django.db import models
from django.contrib.auth.models import User
from .services import FileUploadService


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(to=User, db_index=True, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField()
    bio = models.TextField(max_length=500)
    picture = models.FileField(null=True, upload_to=FileUploadService.profile_picture_path)  # Adjusted to save as user_id.jpg
    is_public = models.BooleanField(default=True)

    class Meta:
        db_table = 'profiles'

class Story(models.Model):
    user = models.ForeignKey(to=User, db_index=True, on_delete=models.CASCADE, related_name='stories')
    attachement = models.FileField(null=True, upload_to=FileUploadService.story_attachement_path)  # Dynamic file path for stories
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stories'

class Follower(models.Model):
    user = models.ForeignKey(to=User, db_index=True, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(to=User, db_index=True, on_delete=models.CASCADE, related_name='followers')
    status = models.BooleanField()

    class Meta:
        db_table = 'followers'
        unique_together = ('user', 'follower')  # To avoid duplicate follows

class Chat(models.Model):
    sender = models.ForeignKey(to=User, db_index=True, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(to=User, db_index=True, on_delete=models.CASCADE, related_name='received_chats')

    class Meta:
        db_table = 'chats'
        unique_together = ('sender', 'receiver')

class Message(models.Model):
    chat = models.ForeignKey(to=Chat, db_index=True, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField(null=True)
    attachement = models.FileField(null=True, upload_to=FileUploadService.message_attachement_path)  # Dynamic file path for chat attachments
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'

