from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import (Chat, Follower, Message, Profile, Story)


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Follower
        fields  = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(required=True)
    bio = serializers.CharField(required=True)
    picture = serializers.FileField(required=True)
    is_public = serializers.BooleanField(required=False)

    user = UserSerializer(read_only=True)
    picture_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_picture_url(self, obj):
        request = self.context.get('request')
        if obj.picture:
            # Use the request to get the full domain and build the complete URL
            return request.build_absolute_uri(obj.picture.url)
        return None


class StorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    attachement_url = serializers.SerializerMethodField()
    class Meta:
        model = Story
        fields = '__all__'
    
    def get_attachement_url(self, obj):
        request = self.context.get('request')
        if obj.attachement:
            return request.get_absolute_uri(obj.attachement.url)
        return None

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)
    attachement_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def validate(self, data):
        if not data.get('message') and not data.get('attachement'):
            raise serializers.ValidationError("Either message or attachment must be provided.")
        return data
    
    def get_attachement_url(self, obj):
        request = self.context.get('request')
        if obj.attachement:
            return request.get_absolute_uri(obj.attachement.url)
        return None

