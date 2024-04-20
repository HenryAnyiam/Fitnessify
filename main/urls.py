from django.urls import path
from .auth import CustomAuthToken
from .views import UserCreateView

urlpatterns = [
            path('api-auth', CustomAuthToken.as_view()),
            path('user', UserCreateView.as_view()),
        ]
