import json

from django.shortcuts import render,redirect,HttpResponse
from df_user import user_decrator as ud
from django.http import JsonResponse
from df_cart import models

# Create your views here.
@ud.login_dec
def cart(request):
    userid=request.session['user_id']
    carts=models.Cart.objects.filter(user_id=userid)
    c = {'page_name': 1, 'cart_name': 1,
         'title': '购物车', 'carts':carts}
    return render(request, 'df_cart/cart.html', c)


@ud.login_dec
def add(request,gid,count):
    gid=int(gid)
    count=int(count)
    userid=request.session['user_id']
    #如果此商品存在就数量加一，不然就创建,carts为Cart类型的集合
    carts=models.Cart.objects.filter(user_id=userid,goods_id=gid)
    if len(carts)>=1:
        cart=carts[0]
        cart.count+=1
    else:
        cart=models.Cart()
        cart.count=1
        cart.goods_id=gid
        cart.user_id=userid
    cart.save()
    if request.is_ajax():
        count=models.Cart.objects.filter(user_id=userid).count()
        return JsonResponse({'count':count})
    else:
        return redirect('/cart/')

@ud.login_dec
def edit(request,cid,gnum):
    ret={'status':200,'error':None}
    try:
        obj=models.Cart.objects.get(pk=int(cid))
        obj.count+=int(gnum)
        obj.save()
    except Exception as e:
        ret['error']="出错了"
        ret['status']=500
    #return HttpResponse(json.dumps(ret))
    return JsonResponse(ret)

@ud.login_dec
def delete(request,cid):
    ret = {'status': 200, 'error': None}
    try:
        obj = models.Cart.objects.get(pk=int(cid))
        obj.delete()
    except Exception as e:
        ret['error'] = "出错了"
        ret['status'] = 500
    # return HttpResponse(json.dumps(ret))
    return JsonResponse(ret)
