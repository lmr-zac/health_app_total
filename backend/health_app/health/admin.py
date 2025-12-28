from django.contrib import admin
from .models import User, SportRecord, DietRecord, HealthIndex

# 注册用户模型
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'height', 'weight', 'create_time')  # 注意字段名和models.py一致
    search_fields = ('username',)  # 末尾的逗号不能少（元组格式）

# 注册运动记录模型
@admin.register(SportRecord)
class SportRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sport_type', 'duration', 'record_date')
    list_filter = ('sport_type', 'record_date')  # 筛选字段和models.py的choices一致

# 注册饮食记录模型
@admin.register(DietRecord)
class DietRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'food_name', 'amount', 'meal_time', 'record_date')
    list_filter = ('meal_time', 'record_date')

# 注册健康指标模型
@admin.register(HealthIndex)
class HealthIndexAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'index_type', 'value', 'record_date')
    list_filter = ('index_type', 'record_date')