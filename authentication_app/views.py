from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
# Create your views here.
def loginUser(request):
    user = authenticate(
        username=request.data.get("user_name"),
        password=request.data.get("password"),
    )
    print(user)
    if user is not None:
        # Delete existing tokens for the user
        Token.objects.filter(user=user).delete()
        # Create a new token
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "token": token.key,
                "msg": "User logged in successfully",
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {
            "status": False,
            "msg": "Invalid credentials",
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    try:
        # Get the token from the request headers
        token = request.auth
        if token:
            token.delete()
            return Response(
                {"msg": "User logged out successfully", "status": True},
                status=status.HTTP_200_OK,
            )
    except Token.DoesNotExist:
        return Response(
            {"msg": "No active session found", "status": False},
            status=status.HTTP_400_BAD_REQUEST,
        )
