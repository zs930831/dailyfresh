from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class TypeInfo(models.Model):
    ttitle=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)

class GoodsInfo(models.Model):
    gname=models.CharField(max_length=30)
    gprice=models.DecimalField(max_digits=6,decimal_places=2)
    gshortintro=models.CharField(max_length=100)
    gstock=models.IntegerField()
    gpic=models.ImageField(upload_to="df_goods")
    gunit=models.CharField(max_length=20)
    isDelet=models.BooleanField(default=False)
    gclick=models.IntegerField()
    gintro=HTMLField()
    gtype=models.ForeignKey(to="TypeInfo",to_field="id")
    #py3里面不需要。
    # def __str__(self):
    #     return self.gname.encode("utf-8")