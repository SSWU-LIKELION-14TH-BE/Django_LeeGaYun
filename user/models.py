from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# 회원 테이블 생성
class CustomUser(AbstractUser): 

    # 실제 로그인용 아이디
    user_id = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set', blank=True)