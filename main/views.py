from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Create your views here.


class UserCreateView(APIView):
    """create a new user"""

    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request, format=None):
        """return current saved users"""

        serializer = UserSerializer(User.objects.all(), many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        """create a new user"""
        serializer = UserSerializer(data=request.data)
        if 'email' not in request.data:
                return Response({'email': "This field is required"},
                                status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            if 'password' not in request.data:
                return Response({'password': "This field is required"},
                                status=status.HTTP_400_BAD_REQUEST)
            new_user = serializer.save()
            new_user.set_password(request.data.get('password'))
            new_user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
