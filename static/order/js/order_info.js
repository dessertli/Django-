$(function () {

    $("#alipay").click(function () {

    //    伪支付
    //    调用支付宝，掉服务器接口，让服务器去支付
    //    蚂蚁金服开放平台，python版本未提供，已提供java，php， .net
    //    RSA 沙箱， python的模拟
    //    企业账号，开通支付宝，认证，创建应用，文档声明一下你要在什么场景下使用支付

        var order_id = $(this).attr("order_id");

        $.getJSON("/axf/alipay/", {"order_id": order_id}, function (data) {
            console.log(data);
            if(data["status"] == "200"){
                window.open("/axf/mine/", target="_self");
            }
        })


    })


})