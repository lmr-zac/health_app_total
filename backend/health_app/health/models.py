# health/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser  # 仅保留这一个用户基类导入

# ========== 唯一的User模型（继承AbstractUser，内置认证字段/管理器，无需重复写） ==========
class User(AbstractUser):
    # 只扩展自定义字段（AbstractUser已内置：username/password/is_staff/is_superuser/is_active等）
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    height = models.FloatField(default=0.0, verbose_name="身高(cm)")
    weight = models.FloatField(default=0.0, verbose_name="体重(kg)")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

# ========== 运动记录模型（无修改，关联上面的User） ==========
class SportRecord(models.Model):
    SPORT_TYPES = [
        ("跑步","跑步"),("快走","快走"),("跳绳","跳绳"),("篮球","篮球"),("羽毛球","羽毛球"),
        ("游泳","游泳"),("骑行","骑行"),("瑜伽","瑜伽"),("健身","健身"),("其他","其他")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    sport_type = models.CharField(max_length=20, choices=SPORT_TYPES, verbose_name="运动类型")
    duration = models.IntegerField(verbose_name="运动时长(分钟)")
    record_date = models.DateField(verbose_name="记录日期")

    class Meta:
        db_table = "sport_record"
        verbose_name = "运动记录"
        verbose_name_plural = verbose_name

# ========== 饮食记录模型 ==========
class DietRecord(models.Model):
    MEAL_TIMES = [("早餐","早餐"),("午餐","午餐"),("晚餐","晚餐"),("加餐","加餐")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    food_name = models.CharField(max_length=50, verbose_name="食材名")
    amount = models.IntegerField(verbose_name="食用量(克)")
    meal_time = models.CharField(max_length=10, choices=MEAL_TIMES, verbose_name="用餐时段")
    record_date = models.DateField(verbose_name="记录日期")

    class Meta:
        db_table = "diet_record"
        verbose_name = "饮食记录"
        verbose_name_plural = verbose_name

# ========== 健康指标模型 ==========
class HealthIndex(models.Model):
    INDEX_TYPES = [("体重","体重"),("收缩压","收缩压"),("舒张压","舒张压"),("心率","心率")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    index_type = models.CharField(max_length=10, choices=INDEX_TYPES, verbose_name="指标类型")
    value = models.FloatField(verbose_name="指标数值")
    record_date = models.DateField(verbose_name="记录日期")

    class Meta:
        db_table = "health_index"
        verbose_name = "健康指标"
        verbose_name_plural = verbose_name