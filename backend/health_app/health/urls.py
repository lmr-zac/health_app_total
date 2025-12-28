# health/urls.py
from django.urls import path
from .views import SportRecordView

urlpatterns = [
    # 错误写法（导致重复api）：path('api/sport/record/', ...)
    # 正确写法（仅保留sport/record/）：
    path('sport/record/', SportRecordView.as_view(), name='sport_record'),
]