# health/views.py
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from .models import SportRecord, DietRecord, HealthIndex
from .serializers import (
    UserSerializer, SportRecordSerializer,
    DietRecordSerializer, HealthIndexSerializer
)

User = get_user_model()

# ========== 用户注册/登录视图 ==========
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)

# 自定义登录视图（返回更多用户信息）
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })

# ========== 运动记录ViewSet（核心：必须定义queryset） ==========
class SportRecordViewSet(viewsets.ModelViewSet):
    serializer_class = SportRecordSerializer
    # 关键：定义queryset（解决basename报错）
    queryset = SportRecord.objects.all()

    # 重写get_queryset：只返回当前登录用户的记录（权限控制）
    def get_queryset(self):
        return SportRecord.objects.filter(user=self.request.user)

    # 重写create：自动关联当前用户
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# （可选）饮食记录ViewSet
class DietRecordViewSet(viewsets.ModelViewSet):
    serializer_class = DietRecordSerializer
    queryset = DietRecord.objects.all()

    def get_queryset(self):
        return DietRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# （可选）健康指标ViewSet
class HealthIndexViewSet(viewsets.ModelViewSet):
    serializer_class = HealthIndexSerializer
    queryset = HealthIndex.objects.all()

    def get_queryset(self):
        return HealthIndex.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)