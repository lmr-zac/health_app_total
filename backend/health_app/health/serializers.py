from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers

from . import models
from .models import SportRecord  # 先导入模型

# 获取自定义User模型（如果用Django内置User，这行也兼容）
User = get_user_model()

# 用户序列化器（注册/返回用户信息用）
class UserSerializer(serializers.ModelSerializer):
    # 注册时需要密码，且返回时隐藏
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']  # 按你的自定义User模型字段调整

    # 重写create方法，确保密码加密存储（关键！）
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# 运动记录序列化器
class SportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportRecord
        fields = ('id', 'sport_type', 'duration', 'record_date')
        extra_kwargs = {'user': {'read_only': True}}  # 用户字段由后端自动关联（避免前端传错）

    # 重写创建方法，自动关联当前登录用户（简化版，新手先这样）
    def create(self, validated_data):
        # 这里暂时先手动传user_id（后续登录后优化为自动获取）
        validated_data['user_id'] = self.context['request'].data.get('user_id')
        return SportRecord.objects.create(**validated_data)


class User(AbstractUser):
    # 自定义字段，比如
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'