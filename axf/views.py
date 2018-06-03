import hashlib
import uuid

from django.core.cache import cache, caches
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.cache import cache_page

from axf.models import Wheel, MainShow, FoodTypes, Goods, UserModel, CartModel, OrderModel, OrderGoodsModel


# Create your views here.
@cache_page(60)
def home(request):
    print("获取数据了")
    sliderList = Wheel.objects.all()
    mainShowList = MainShow.objects.all()
    return render(request, "home/home.html", {"sliderList": sliderList, "mainShowList": mainShowList})

def market(request):
    return redirect(reverse("axf:marketWithParams", args=("104749", "0", "0")))

# order_rule    0 代表默认排序，   1 代表销量排序   2， 价格升高排序   3， 价格降低排序
def marketWithParams(request, categoryid, cid, order_rule):

    # 第一步去缓存中获取，缓存中存在，直接返回，如果不存在，应该去数据库查询，添加到缓存中，做一个返回
    # cache = caches["default"]

    result = cache.get("marketWithParams")

    if result:
        print("从缓存中获取数据")
        return HttpResponse(result)

    # 分组信息
    leftMenuList = FoodTypes.objects.all()

    if cid == "0":
        goodsList = Goods.objects.filter(categoryid=categoryid)
    else:
        goodsList = Goods.objects.filter(categoryid=categoryid).filter(childcid=cid)


    if order_rule == "1":
        # 销量排序
        goodsList = goodsList.order_by("-productnum")
    elif order_rule == "2":
        # 价格升序
        goodsList = goodsList.order_by("-price")
    elif order_rule == "3":
        # 价格降序
        goodsList = goodsList.order_by("price")
    else:
        pass

    childtype = FoodTypes.objects.get(typeid=categoryid)

    print(childtype.childtypenames)

    childtypes = childtype.childtypenames.split("#")

    print(childtypes)

    childtype_items = []

    for item in childtypes:
        childitems = item.split(":")
        childtype_items.append(childitems)

    data = {
        "leftMenuList": leftMenuList,
        "goodsList": goodsList,
        "childtype_items": childtype_items,
        "categoryid": categoryid,
        "childtypeid": cid,
    }
    # ① 加载  ② 渲染
    # render(request, "market/market.html", context=data)
    print("从数据库中查询数据")
    template = loader.get_template("market/market.html")
    content = template.render(data)

    cache.set("marketWithParams", content, timeout=30)

    return HttpResponse(content)


def products(request):
    productid = request.GET.get("pd")
    print("*********************", productid)
    return JsonResponse({"data": "sunck is a good man"})


def cart(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect(reverse("axf:user_login"))

    carts = CartModel.objects.filter(user_id=user_id)

    is_all_select = True

    for cart_obj in carts:
        if not cart_obj.is_select:
            is_all_select = False
            break

    data = {
        "carts": carts,
        "is_all_select": is_all_select
    }
    return render(request, "cart/cart.html", context=data)


def mine(request):

    user_id = request.session.get("user_id")

    print(user_id)

    users = UserModel.objects.filter(pk=user_id)

    data = {

    }

    if users.exists():
        user = users.first()

        username = user.username
    # url 是相对于MEDIA_ROOT的
        icon = user.icon.url

        print(icon)

        data["username"] = username

        data["icon_url"] = "/static/uploads/" + icon
        # user = UserModel()
        data["wait_receive_num"] = user.ordermodel_set.filter(o_status=1).count()

        data["wait_pay_num"] = user.ordermodel_set.filter(o_status=0).count()

    return render(request, "mine/mine.html", context=data)


def user_register(request):
    return render(request, 'user/register.html')


def do_user_register(request):

    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    icon = request.FILES.get("icon")

    print(password)

    user = UserModel()
    user.username = username
    user.password = generate_password(password)
    user.email = email
    user.icon = icon

    user.save()

    request.session['user_id'] = user.id

    return redirect(reverse("axf:mine"))


def generate_password(pa):
    # md5 hashlib
    md5 = hashlib.md5()

    md5.update(pa.encode("utf-8"))

    pa = md5.hexdigest()

    return pa


def user_logout(request):
    request.session.flush()
    return redirect(reverse("axf:mine"))


def user_login(request):
    return render(request, 'user/login.html')


def do_user_login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    users = UserModel.objects.filter(username=username)

    if users.exists():
        user = users.first()
        password_user = user.password
        if password_user == generate_password(password):
            request.session["user_id"] = user.id
            return redirect(reverse("axf:mine"))

    return redirect(reverse("axf:user_login"))


def add_to_cart(request):
    goodsid = request.GET.get("goodsid")

    user_id = request.session.get("user_id")

    data = {
        "msg": "ok",
        "status": "200",
    }

    if not user_id:
    #     实现用户跳转到登录界面, 重定向（不能实现）
        data["status"] = "901"
        data["msg"] = "not login"
        return JsonResponse(data=data)
    carts = CartModel.objects.filter(user_id=user_id).filter(goods_id=goodsid)
    if carts.exists():
        cart_obj = carts.first()
        cart_obj.goods_num = cart_obj.goods_num + 1
        cart_obj.save()
        data["goods_num"] = cart_obj.goods_num
    else:
        cart_obj = CartModel()
        cart_obj.user_id = user_id
        cart_obj.goods_id = goodsid
        cart_obj.save()
        data["goods_num"] = cart_obj.goods_num

    return JsonResponse(data=data)


def sub_to_cart(request):

    goodsid = request.GET.get("goodsid")

    user_id = request.session.get("user_id")

    data = {
        "msg": "ok",
        "status": "200",
    }

    # ide 通常都有万能键   alt + enter
    if not user_id:
        data["status"] = "901"
        data["msg"] = "not login"
        return JsonResponse(data=data)

    carts = CartModel.objects.filter(user_id=user_id).filter(goods_id=goodsid)

    if carts.exists():
        cart_obj = carts.first()
        # 只有一个数量，直接将此条购物数据删除就ok
        if cart_obj.goods_num == 1:
            cart_obj.delete()
            data["goods_num"] = "0"
            data["msg"] = "delete success"
        else:
            cart_obj.goods_num = cart_obj.goods_num - 1
            cart_obj.save()
            data["goods_num"] = cart_obj.goods_num

    return JsonResponse(data=data)


def sub_cart(request):
    cart_id = request.GET.get("cartid")

    carts = CartModel.objects.filter(pk=cart_id)

    data = {
        "msg": "ok",
        "status": "200"
    }

    if carts.exists():
        cart_obj = carts.first()
        if cart_obj.goods_num == 1:
            cart_obj.delete()
            data["goods_num"] = "0"
            # 902 商品被彻底删除
            data["status"] = "902"
            data["msg"] = "数据已彻底删除"
        else:
            cart_obj.goods_num = cart_obj.goods_num - 1
            cart_obj.save()
            data["goods_num"] = cart_obj.goods_num

    return JsonResponse(data=data)


def add_cart(request):
    cart_id = request.GET.get("cartid")

    carts = CartModel.objects.filter(pk=cart_id)

    data = {
        "msg": "ok",
        "status": "200",
    }

    if carts.exists():
        cart_obj = carts.first()
        cart_obj.goods_num = cart_obj.goods_num + 1
        cart_obj.save()
        data["goods_num"] = cart_obj.goods_num

    return JsonResponse(data=data)

"""
    如果出现了一个未选中
        全选按钮就变成未选中
    如果所有都变成选中
        全选按钮也变成选中

"""
def cart_change_check(request):
    cart_id = request.GET.get("cartid")

    cart = CartModel.objects.get(pk=cart_id)

    cart.is_select = not cart.is_select

    cart.save()

    is_all_select = True

    user_id = request.session.get("user_id")

    carts = CartModel.objects.filter(user_id=user_id)

    for cart_obj in carts:
        if not cart_obj.is_select:
            is_all_select = False

    data = {
        "msg": "ok",
        "status": "200",
        "is_select": cart.is_select,
        "is_all_select": is_all_select,
    }

    return JsonResponse(data=data)


def all_select(request):

    selects = request.GET.get("selects")

    select_list = selects.split("#")

    print(select_list)

    data = {
        "msg": "ok",
        "status": "200",
    }

    for select in select_list:
        cart_obj = CartModel.objects.get(pk=select)
        cart_obj.is_select = False
        cart_obj.save()

    data["selects"] = selects

    return JsonResponse(data = data)


def all_selects(request):
    unselects = request.GET.get("selects")

    unselect_list = unselects.split("#")

    for unselect in unselect_list:
        cart_obj = CartModel.objects.get(pk=unselect)
        cart_obj.is_select = True
        cart_obj.save()

    data = {
        "status": "200",
        "msg": "ok",
        "selects": unselects
    }

    return JsonResponse(data= data)


def generate_order(request):
    # 接收到需要购买的商品信息
    selects = request.GET.get("selects")
    select_list = selects.split("#")
    # 生成一个新的订单
    order = OrderModel()

    user_id = request.session.get("user_id")
    order.o_user_id = user_id
    # 唯一标识  uuid广泛使用的唯一标识  使用了纳秒级的时间，硬件设备的mac地址
    order.o_num = str(uuid.uuid4())

    order.save()

    data = {
        "msg": "ok",
        "status": "200",
        "order_id":order.id
    }

    # 将购买信息在OrderGoods中生成
    for select in select_list:
        order_goods = OrderGoodsModel()
        cart_obj = CartModel.objects.get(pk=select)
        order_goods.og_order_id = order.id
        order_goods.og_goods_id = cart_obj.goods_id
        order_goods.og_num = cart_obj.goods_num
        order_goods.save()
        cart_obj.delete()

    # 删除购物车中已购买的商品
    return JsonResponse(data=data)


def order_info(request, order_id):

    order = OrderModel.objects.get(pk=order_id)

    data = {
        "order": order,
    }

    return render(request, 'order/OrderInfo.html', context=data)


def alipay(request):
    order_id = request.GET.get("order_id")
    order = OrderModel.objects.get(pk=order_id)

    order.o_status = 1
    order.save()

    data = {
        "msg": "ok",
        "status": "200",
    }

    return JsonResponse(data=data)