from django.db import models

# Create your models here.
class Cart(models.Model):
    #物理删除，不用逻辑删除
    user=models.ForeignKey('df_user.UserInfo')
    goods=models.ForeignKey(to='df_goods.GoodsInfo')
    count=models.IntegerField()