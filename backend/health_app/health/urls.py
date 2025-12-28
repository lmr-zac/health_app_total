# health/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import SportRecordView

router = DefaultRouter()
router.register(r'sport-records', views.SportRecordViewSet)  # 自动生成列表、新增、修改、删除路由

urlpatterns = [
    # 1. 运动记录接口（列表+新增，基于你当前的ListCreateAPIView）
    path('sport-records/', views.SportRecordView.as_view(), name='sport-records'),

    # 2. 补充运动记录的修改/删除（如果后续换成ModelViewSet会更简洁，先兼容当前代码）
    # 若后续替换为ModelViewSet，这两行可删，用router替代
    path('sport-records/<int:pk>/', views.SportRecordDetailView.as_view(), name='sport-record-detail'),

    # 3. 用户认证接口
    path('register/', views.UserRegisterView.as_view(), name='user-register'),  # 注册
    path('login/', views.CustomAuthToken.as_view(), name='user-login'),  # 登录（自定义返回Token）
    # 可选：默认登录接口（仅返回Token，字段简单）
    # path('login-default/', obtain_auth_token, name='login-default'),
]