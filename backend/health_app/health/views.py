from rest_framework import generics

from .models import SportRecord
from .serializers import SportRecordSerializer

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