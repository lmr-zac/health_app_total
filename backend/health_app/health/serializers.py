from rest_framework import serializers
from .models import SportRecord  # 先导入模型

# 运动记录序列化器
class SportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportRecord
        fields = ('id', 'user', 'sport_type', 'duration', 'record_date')
        extra_kwargs = {'user': {'read_only': True}}  # 用户字段由后端自动关联（避免前端传错）

    # 重写创建方法，自动关联当前登录用户（简化版，新手先这样）
    def create(self, validated_data):
        # 这里暂时先手动传user_id（后续登录后优化为自动获取）
        validated_data['user_id'] = self.context['request'].data.get('user_id')
        return SportRecord.objects.create(**validated_data)