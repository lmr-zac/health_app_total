from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
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

# 1. 用户管理器（必须定义，用于创建用户和超级用户）
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('必须设置用户名')
        user = self.model(username=username,** extra_fields)
        user.set_password(password)  # 加密存储密码
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password,** extra_fields)

# 2. 用户表（继承认证基类）
class User(AbstractBaseUser, PermissionsMixin):  # 修改继承
    username = models.CharField(max_length=50, unique=True, verbose_name="账号")
    password = models.CharField(max_length=100, verbose_name="密码")  # 可保留，或通过AbstractBaseUser的set_password处理
    height = models.FloatField(default=0.0, verbose_name="身高(cm)")
    weight = models.FloatField(default=0.0, verbose_name="体重(kg)")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")  # 新增：认证必要字段
    is_staff = models.BooleanField(default=False, verbose_name="是否为管理员")  # 新增：控制后台访问权限

    # 认证系统必要配置
    objects = UserManager()  # 关联用户管理器
    USERNAME_FIELD = 'username'  # 登录时使用的字段（这里是username）
    REQUIRED_FIELDS = []  # 解决报错的核心：定义必要字段（根据需要添加，如邮箱等）

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name