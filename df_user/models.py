from django.db import models

# Create your models here.
class UserInfo(models.Model):
    #defalut和blank的添加不用迁移，因为之影响了python层面
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=20)
    uaddress=models.CharField(max_length=50,default='')
    ushouaddress = models.CharField(max_length=50,default='')
    uemail = models.CharField(max_length=20)
    uphonenum = models.CharField(max_length=11,default='')
    uyoubian=models.CharField(max_length=7,default='')


