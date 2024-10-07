from .serializers import UserSerializer
from django.contrib.auth import authenticate
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey


@api_view(['POST'])
def loginUser(request):
    username = request.data.get('user_name')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(username=username, password=password)
    if user is not None:
        # Delete any existing API keys for the user
        APIKey.objects.filter(name=user.username).delete()  # Ensure user has no old keys
        
        # Create a new API key for the user with an expiry date
        expiration_time = timezone.now() + timedelta(days=1)  # 1 day validity
        api_key, key = APIKey.objects.create_key(name=user.username, expiry_date=expiration_time)

        return Response({
            'user': UserSerializer(user).data,  # Return the username instead of the user object
            'api_key': key,
            'status': True
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([HasAPIKey])
def logoutUser(request):
    # Get API key from Authorization header
    api_key_header = request.headers.get('Authorization')

    if not api_key_header:
        return Response({'error': 'API key required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Extract API key from the Authorization header
        api_key = api_key_header.split(' ')[1]  # Expects format like "Api-Key YOUR_API_KEY"
        api_key_obj = APIKey.objects.get_from_key(api_key)
        api_key_obj.delete()  # Invalidate the API key
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except (APIKey.DoesNotExist, IndexError):
        return Response({'error': 'Invalid or missing API key'}, status=status.HTTP_400_BAD_REQUEST)
