# health/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SportRecord, DietRecord, HealthIndex

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 注意：create_time 是自定义字段，AbstractUser 内置 date_joined（创建时间），可二选一
        fields = ['id', 'username', 'password', 'phone', 'height', 'weight', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # 最稳妥写法：手动创建+加密密码，避开 create_user 参数陷阱
        password = validated_data.pop('password')  # 移除密码，手动加密
        user = User.objects.create(**validated_data)  # 创建用户（包含username/phone等）
        user.set_password(password)  # 加密密码（核心）
        user.save()  # 保存密码修改
        return user