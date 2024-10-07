from django.urls import path, include
from .user_management_views.user_view_set import UserViewSet
from .user_management_views.profile_view_set import ProfileViewSet
from .user_management_views.follower_view_set import FollowerViewSet
from .user_management_views.chat_view_set import ChatViewSet
from .user_management_views.story_view_set import StoryViewSet
from .user_management_views.message_view_set import MessageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"user", UserViewSet, basename="user")
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"chat", ChatViewSet, basename="chat")
router.register(r"message", MessageViewSet, basename="message")
router.register(r"story", StoryViewSet, basename="story")
router.register(r"follower", FollowerViewSet, basename="follower")


urlpatterns = [
    path("", include(router.urls)),
]
