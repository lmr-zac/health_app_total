# health/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 初始化路由器
router = DefaultRouter()

# 方式1：依赖ViewSet的queryset（推荐，已在views.py定义queryset）
router.register(r'sport-records', views.SportRecordViewSet)
# 可选：注册其他ViewSet
router.register(r'diet-records', views.DietRecordViewSet)
router.register(r'health-indexes', views.HealthIndexViewSet)

# 方式2：若ViewSet无queryset，手动指定basename（备用）
# router.register(r'sport-records', views.SportRecordViewSet, basename='sport-record')

# 非ViewSet的路由（注册/登录）
urlpatterns = [
    path('', include(router.urls)),  # 挂载ViewSet路由
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.CustomAuthToken.as_view(), name='user-login'),
]