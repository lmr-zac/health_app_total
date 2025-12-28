# health_backend/urls.py
from django.contrib import admin
from django.urls import path, include  # 必须导入include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 仅保留这一行，删除所有其他sport/record相关路由
    path('api/', include('health.urls')),
]