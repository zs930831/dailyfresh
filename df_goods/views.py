from django.shortcuts import render
from df_goods import models
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    type = models.TypeInfo.objects.all()
    # 按照最新，最新的id最大
    type0 = type[0].goodsinfo_set.order_by('-id')[0:4]
    # 按照点击热度，热度越大，点击量越大
    type01 = type[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = type[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = type[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = type[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = type[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = type[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = type[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = type[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = type[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = type[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = type[5].goodsinfo_set.order_by('-gclick')[0:4]
    c = {'title': '首页', 'guest_cart': 1,
         'type0': type0, 'type01': type01,
         'type1': type1, 'type11': type11,
         'type2': type2, 'type21': type21,
         'type3': type3, 'type31': type31,
         'type4': type4, 'type41': type41,
         'type5': type5, 'type51': type51}
    return render(request, "df_goods/index.html", c)


def detail(request, gid):
    goods = models.GoodsInfo.objects.get(pk=gid)
    goods.gclick += 1
    goods.save()
    news=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    c = {'title': goods.gname, 'guest_cart': 1,
         'goods':goods,"news":news}
    resp = render(request, "df_goods/detail.html", c)
    #下面给用户中心使用
    return resp


def list(request, tid, pindex, sort):
    print(tid, pindex, sort)
    typeinfo = models.TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == "1":  # 默认最新
        good_list = typeinfo.goodsinfo_set.order_by('-id')
    elif sort == "2":  # 价格从低到高
        good_list = typeinfo.goodsinfo_set.order_by('gprice')
    elif sort == "3":  # 最热
        good_list = typeinfo.goodsinfo_set.order_by('-gclick')
    # 总页数
    paginator = Paginator(good_list, 10)
    # 当前页面,下一页，上一页,里面有good_list对象
    page = paginator.page(int(pindex))
    c = {'title': typeinfo.ttitle, 'guest_cart': 1,
         "typeinfo": typeinfo, "news": news,
         'good_list': good_list, "paginator": paginator, "sort": sort,
         'page': page}
    return render(request, "df_goods/list.html", c)
