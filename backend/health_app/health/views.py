from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SportRecord, User
from .serializers import SportRecordSerializer, UserSerializer

# 运动记录详情视图（修改/删除）
class SportRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SportRecordSerializer
    permission_classes = [IsAuthenticated]  # 仅登录用户可操作

    # 只允许操作当前用户的记录（防止越权）
    def get_queryset(self):
        return SportRecord.objects.filter(user=self.request.user)

# 运动记录列表+新增接口
class SportRecordView(generics.ListCreateAPIView):
    queryset = SportRecord.objects.all()
    serializer_class = SportRecordSerializer

    # 支持按用户筛选（前端传user_id）
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return SportRecord.objects.filter(user_id=user_id)
        return SportRecord.objects.all()

# 注册接口
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)

# 登录接口（获取token）
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })

class SportRecordViewSet(viewsets.ModelViewSet):
    serializer_class = SportRecordSerializer
    permission_classes = [IsAuthenticated]  # 仅登录用户可访问

    # 只查询当前登录用户的运动记录
    def get_queryset(self):
        return SportRecord.objects.filter(user=self.request.user)

    # 新增记录时自动关联当前用户
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)