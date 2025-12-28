# health/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import SportRecordView

router = DefaultRouter()
router.register(r'sport-records', views.SportRecordViewSet)  # 自动生成列表、新增、修改、删除路由

urlpatterns = [
    # 错误写法（导致重复api）：path('api/sport/record/', ...)
    # 正确写法（仅保留sport/record/）：
    path('sport/record/', SportRecordView.as_view(), name='sport_record'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
]