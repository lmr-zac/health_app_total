from django.db import models

# 1. 用户表（账号、密码、身高体重）
class User(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name="账号")  # 账号唯一
    password = models.CharField(max_length=100, verbose_name="密码")
    height = models.FloatField(default=0.0, verbose_name="身高(cm)")
    weight = models.FloatField(default=0.0, verbose_name="体重(kg)")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "user"  # 数据库表名不变，仍为user
        verbose_name = "用户"
        verbose_name_plural = verbose_name

# 2. 运动记录表（预设10种运动类型）
class SportRecord(models.Model):
    SPORT_TYPES = [("跑步","跑步"),("快走","快走"),("跳绳","跳绳"),("篮球","篮球"),("羽毛球","羽毛球"),
                   ("游泳","游泳"),("骑行","骑行"),("瑜伽","瑜伽"),("健身","健身"),("其他","其他")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    sport_type = models.CharField(max_length=20, choices=SPORT_TYPES, verbose_name="运动类型")
    duration = models.IntegerField(verbose_name="运动时长(分钟)")
    record_date = models.DateField(verbose_name="记录日期")

    class Meta:
        db_table = "sport_record"
        verbose_name = "运动记录"
        verbose_name_plural = verbose_name

# 3. 饮食记录表（预设用餐时段）
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

# 4. 健康指标表（仅4种核心指标）
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