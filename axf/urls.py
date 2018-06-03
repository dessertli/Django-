from django.conf.urls import url
from axf import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.marketWithParams, name='marketWithParams'),
    url(r'^products/', views.products, name='products'),

    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^userregister/', views.user_register, name='user_register'),
    url(r'^douserregister/', views.do_user_register, name='do_user_register'),
    url(r'^userlogout/', views.user_logout, name='user_logout'),
    url(r'^userlogin/', views.user_login, name='user_login'),
    url(r'^douserlogin/', views.do_user_login, name='do_user_login'),
    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),
    url(r'^subtocart/', views.sub_to_cart, name='sub_to_Cart'),
    url(r'^subcart/', views.sub_cart, name='sub_cart'),
    url(r'^addcart/', views.add_cart, name='add_cart'),
    url(r'^cartchangecheck/', views.cart_change_check, name='cart_change_check'),
    url(r'^allselect/', views.all_select, name='all_select'),
    url(r'^allselects/', views.all_selects, name='all_selects'),
    url(r'^generateorder/', views.generate_order, name="generate_order"),
    url(r'^orderinfo/(\d+)/', views.order_info, name="order_info"),
    url(r'^alipay/', views.alipay, name='alipay'),
]