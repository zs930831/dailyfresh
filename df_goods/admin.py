from django.contrib import admin
from df_goods import models


# Register your models here.
@admin.register(models.TypeInfo)
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'gname', 'gprice','gshortintro','gstock',
                    'gunit','gclick','gintro','gtype']


admin.site.register(models.GoodsInfo, GoodsInfoAdmin)
