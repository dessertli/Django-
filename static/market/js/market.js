$(document).ready(function(){

    $("#allTypeBtn").click(function () {

        $("#type_container").show();

    })

    $("#type_container").click(function () {
        $(this).hide();
    })

    $("#allSortBtn").click(function () {
        $("#order_container").show();
    })

    $("#order_container").click(function () {
        $(this).hide();
    })


//    添加到购物车
    $(".addShopping").click(function () {
        var addShopping = $(this);
        var goodsid = $(this).attr("goodsid");
        console.log(goodsid);
    //    ajax 网络请求，  get post, 还可以设置返回数据的格式， JSON
        $.getJSON("/axf/addtocart/", {"goodsid": goodsid}, function (data) {
            console.log(data);
            if(data["status"] == "901"){
                window.open("/axf/userlogin/", target="_self");
            }else if(data["status"] == "200"){
                var goods_num = data["goods_num"];
                addShopping.prev().html(goods_num);
            }
        })
    })


    $(".subShopping").click(function () {
        var subShopping = $(this);
        var goodsid = $(this).attr("goodsid");

        console.log(goodsid);

        $.getJSON("/axf/subtocart/", {"goodsid": goodsid}, function (data) {
            console.log(data);
            if (data["status"] == "901"){
                window.open("/axf/userlogin/", target="_self");
            }else if(data["status"] == "200"){
                var goods_num = data["goods_num"];
                subShopping.next().html(goods_num);
            }
        })

    })

});