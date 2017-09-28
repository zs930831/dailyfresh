from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from df_user.models import UserInfo
from df_goods import models as m1
from df_orders.models import *
from df_user import user_decrator as ud
from django.core.paginator import Paginator
from django.db import transaction

import hashlib


# Create your views here.
def register(request):
    return render(request, "ds_user/register.html", {"title": "注册"})


def register_handler(request):
    # 接受从register.html传过来的数据
    post = request.POST
    uname = post.get("user_name")
    upwd = post.get("pwd")
    upwd1 = post.get("cpwd")
    uemail = post.get("email")
    if uname == '' or upwd == '' or upwd1 == '' or uemail == '':
        return redirect('/user/register/')
    # 判断俩次密码是否相同
    if upwd != upwd1:
        return redirect("/user/register/")
    # 密码加密
    s1 = hashlib.sha1()
    # 注意update()必须指定要加密的字符串的字符编码
    s1.update(upwd1.encode("utf-8"))
    upwd2 = s1.hexdigest()
    # 在数据库里面创建新用户
    UserInfo.objects.create(
        uname=uname,
        upwd=upwd2,
        uemail=uemail,
    )
    return redirect('/user/login')


def register_yz(request):
    username = request.GET.get('username')
    count = UserInfo.objects.filter(uname=username).count()
    return JsonResponse({"count": count})


def login(request):
    uname = request.COOKIES.get('username', '')
    c = {"user_error1": 0, "pwd_error1": 0, "title": '用户登录', 'username': uname}
    return render(request, "ds_user/login.html", c)


def logout(request):
    # 清除用户所有的session
    # clear()：清除所有会话
    # flush()：删除当前的会话数据并删除会话的Cookie
    # del request.session['_id']：删除会话
    request.session.flush()
    return redirect('/')


def login_handler(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    checkd = post.get('check', 0)
    user = UserInfo.objects.filter(uname=uname)
    if len(user) == 1:  # 存在用户名
        # 密码加密
        s1 = hashlib.sha1()
        # 注意update()必须指定要加密的字符串的字符编码
        s1.update(upwd.encode("utf-8"))
        upwd2 = s1.hexdigest()
        if upwd2 == user[0].upwd:  # 密码正确
            url = request.COOKIES.get('url', '/')
            result = HttpResponseRedirect(url)
            if checkd != 0:
                result.set_cookie('username', uname)
            else:
                result.set_cookie('username', uname, max_age=-1)
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return result
        else:
            # print("pwd error")
            c = {"user_error1": 0, "pwd_error1": 1, "title": '用户登录', 'username': uname, 'upwd': upwd}
            return render(request, "ds_user/login.html", c)

    else:
        # print("user error")
        c = {"user_error1": 1, "pwd_error1": 0, "title": '用户登录', 'username': uname, 'upwd': upwd}
        return render(request, "ds_user/login.html", c)


@ud.login_dec
def info(request):
    # listnum=[i for i in range(3,8)]
    uname = request.session['user_name']
    user = UserInfo.objects.filter(id=request.session['user_id'])
    goods_ids = request.COOKIES.get('goods_ids', None)
    goods_list = []
    if goods_ids != None:
        for i in goods_ids.split(','):
            goods_list.append(m1.GoodsInfo.objects.get(pk=int(i)))
    # print(user[0].id)
    c = {"title": '用户信息', "username": uname, "user": user[0],
         "listnum": range(3, 8), 'page_name': 1,
         "goods_list": goods_list}
    return render(request, 'ds_user/user_center_info.html', c)


@ud.login_dec
def center(request, pindex):
    uid = request.session.get('user_id', None)
    if uid == None:
        return redirect('/user/login')
    order = OrderInfo.objects.filter(user_id=int(uid))
    orderdetaillist = []
    for o in order:
        orderdetaillist.append(OrderDetailInfo.objects.filter(order_id=o.oid))
    paginator = Paginator(orderdetaillist, 1)
    # 当前页面,下一页，上一页,里面有orderdetaillist对象
    page = paginator.page(int(pindex))
    c = {"title": '用户订单', 'page_name': 1,
         'page': page, "paginator": paginator, }
    return render(request, 'ds_user/user_center_order.html', c)


@ud.login_dec
def adress(request):
    user = UserInfo.objects.filter(id=request.session['user_id'])
    if request.method == "POST":
        post = request.POST
        uname = post.get('username')
        detail = post.get('detail')
        yb = post.get('yb')
        phone = post.get('phone')
        user.update(uname=uname, ushouaddress=detail, uyoubian=yb, uphonenum=phone)
        return redirect('/user/address')
    c = {"title": '用户地址', "user": user[0], 'page_name': 1}
    return render(request, 'ds_user/user_center_site.html', c)

@transaction.atomic()
@ud.login_dec
def pay(request,oid,pindex):
    tran_id=transaction.savepoint()
    try:
        order=OrderInfo.objects.get(oid=int(oid))
        order.oIsPay=1
        order.save()
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('=====================%s'%e)
        transaction.savepoint_rollback(tran_id)
    return redirect('/user/center/'+pindex+'/')

def orm(request):
    for i in range(1, 7):
        for j in range(21, 40):
            m1.GoodsInfo.objects.create(gname="维多利亚葡萄" + str(j), gprice=str(j + 30), gshortintro='好吃的葡萄' + str(j),
                                        gstock=100,
                                        gpic='images/goods/goods002.jpg', gunit='500克', gclick=10000 + j,
                                        gintro='好吃的葡萄真的特别好吃' + str(j), gtype_id=i)
    return HttpResponse("ok")
