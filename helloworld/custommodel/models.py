from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 添加额外字段
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    verify_code = models.CharField(max_length=6, blank=True, null=True)

    # 如果需要使用电子邮件作为唯一标识符
    # email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

class Message(models.Model):
    message_id=models.TextField(max_length=100)
    content = models.TextField()  # 消息内容
    message_type = models.CharField(max_length=20, default='text')  # 消息类型，如 text, image, file 等
    phone_number = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)  # 自动记录创建时间
    user_flag=models.BooleanField(default=False)
    # title=models.TextField(max_length=100,blank=True)
    # class Meta:
    #     ordering = ['-timestamp']  # 按时间倒序排列

class Msg_title(models.Model):
    message_id=models.TextField(max_length=100)
    phone_number = models.CharField(max_length=15)
    title=models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)  # 自动记录创建时间


class LoginRecord(models.Model):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    verify_code = models.CharField(max_length=6, blank=True, null=True)

    sendtime=models.DateTimeField(auto_now=True)
