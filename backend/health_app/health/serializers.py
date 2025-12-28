from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers

from . import models
from .models import SportRecord, DietRecord, HealthIndex  # 先导入模型

# 获取自定义User模型（如果用Django内置User，这行也兼容）
User = get_user_model()

# ========== 用户序列化器 ==========
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 字段仅保留自定义+核心认证字段（AbstractUser内置字段已包含）
        fields = ['id', 'username', 'password', 'phone', 'height', 'weight', 'create_time']
        extra_kwargs = {'password': {'write_only': True}}  # 密码只写不返回

    # 重写create方法：使用AbstractUser内置的create_user（自动加密密码）
    def create(self, validated_data):
        # 提取密码（AbstractUser的create_user需要单独传密码）
        password = validated_data.pop('password')
        # 创建用户（自动加密密码，无需手动set_password）
        user = User.objects.create_user(
            username=validated_data['username'],
            password=password,  # 核心：密码单独传，自动加密
            **validated_data    # 其他字段（phone/height/weight）
        )
        return user

# ========== 运动记录序列化器（自动关联当前登录用户） ==========
class SportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportRecord
        fields = ['id', 'sport_type', 'duration', 'record_date']  # 移除user字段（后端自动关联）

    # 登录后：新增记录时自动关联当前用户（无需前端传user_id）
    def create(self, validated_data):
        # 从请求上下文获取当前登录用户
        user = self.context['request'].user
        # 自动关联用户并创建记录
        return SportRecord.objects.create(user=user,** validated_data)

# （可选）饮食/健康指标序列化器（同运动记录逻辑）
class DietRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietRecord
        fields = ['id', 'food_name', 'amount', 'meal_time', 'record_date']

    def create(self, validated_data):
        user = self.context['request'].user
        return DietRecord.objects.create(user=user, **validated_data)

class HealthIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthIndex
        fields = ['id', 'index_type', 'value', 'record_date']

    def create(self, validated_data):
        user = self.context['request'].user
        return HealthIndex.objects.create(user=user,** validated_data)
