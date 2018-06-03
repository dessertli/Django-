from django.db import models

# Create your models here.


#轮播模型
class Wheel(models.Model):
    img = models.CharField(max_length=256)
    name = models.CharField(max_length=32)
    trackid = models.CharField(max_length=32)

class MainShow(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=20)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=50)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=50)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=50)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)




# 分类模型
class FoodTypes(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField()
    childtypenames = models.CharField(max_length=150)


# 商品模型
"""
insert into axf_goods
(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,
categoryid,childcid,childcidname,dealerid,storenums,productnum) values
("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q","",
"乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4);

"""
class Goods(models.Model):
    productid = models.CharField(max_length=16)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=0)
    pmdesc = models.CharField(max_length=16)
    specifics = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.CharField(max_length=16)
    childcid = models.CharField(max_length=16)
    childcidname = models.CharField(max_length=32)
    dealerid = models.CharField(max_length=32)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)


class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)
    # 密码 不允许密码明文传输， 密码也是加密的数据 不可逆加密方式 ，摘要算法md5， sha
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    # 头像字段  存储的是路径
    icon = models.ImageField(upload_to='icons')
    is_delete = models.BooleanField(default=False)


# 购物车模型
class CartModel(models.Model):
    user = models.ForeignKey(UserModel)
    goods = models.ForeignKey(Goods)
    goods_num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)


class OrderModel(models.Model):
    o_num = models.CharField(max_length=128)
    o_user = models.ForeignKey(UserModel)
    o_status = models.IntegerField(default=0)
    o_create_time = models.DateTimeField(auto_now=True)


class OrderGoodsModel(models.Model):
    og_order = models.ForeignKey(OrderModel)
    og_goods = models.ForeignKey(Goods)
    og_num = models.IntegerField(default=1)


