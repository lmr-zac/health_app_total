# health/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, SportRecord, HealthIndex, DietRecord  # 确保导入了SportRecord模型


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

# 补充运动记录序列化器（关键缺失部分）
class SportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportRecord  # 关联到models.py中的SportRecord模型
        # 根据你的SportRecord模型实际字段调整fields
        fields = ['id', 'user', 'sport_type', 'duration',  'record_date']  # 示例字段，需与模型一致
        
# ========== 【新增】健康指标序列化器（如果views.py导入了，必须定义） ==========
class HealthIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthIndex  # 关联models.py的HealthIndex模型
        fields = ['id', 'index_type', 'value', 'record_date']  # 匹配模型字段
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        return HealthIndex.objects.create(user=user,** validated_data)


# ========== 饮食记录序列化器（必须完整定义，不能只写pass） ==========
class DietRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietRecord  # 关联models.py的DietRecord模型
        fields = ['id', 'food_name', 'amount', 'meal_time', 'record_date']  # 匹配模型字段
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        return DietRecord.objects.create(user=user, **validated_data)