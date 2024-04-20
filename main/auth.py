from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

class CustomUserAuthenticationBackend(ModelBackend):
    """custom user authentication"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """authenticate a user by username"""

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None



class CustomAuthToken(ObtainAuthToken):
    """token  for user"""

    def post(self, request, *args, **kwargs):
        """post token data"""

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
