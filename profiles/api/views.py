from rest_framework import permissions
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Profile, TargetCalories
from .serializers import UserSerializer, ProfileSerializer, TargetCaloriesSerializer
import datetime
from django.db.models import Sum, Avg

User = get_user_model()


@api_view(['GET', ])
def profile_homepage_api_view(request, format=None):
    return Response({
        "access_token": reverse("token_obtain_pair", request=request, format=format),
        "token_refresh": reverse("token_refresh", request=request, format=format),
        "register": reverse("api_profile:register", request=request, format=format),
        "profile": reverse("api_profile:profile", request=request, format=format),
        "target": reverse("api_profile:target", request=request, format=format),

    })


class UserRegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        user = self.request.user
        self.user = user
        profile = Profile.objects.get(user=user)
        return profile

    def get(self, request, format=None):
        profile = self.get_object()
        serializer = ProfileSerializer(profile)
        data = serializer.data
        data['username'] = self.user.username
        return Response(data)


class CaloriesTargetApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        profile = self.request.user.profile
        targets = TargetCalories.objects.filter(profile=profile)
        return targets.first() if targets.exists() else None

    def get(self, request, format=None):
        obj = self.get_object()
        if obj is None:
            return Response({'target': 'No Object'})
        data = TargetCaloriesSerializer(obj).data
        return Response(data)