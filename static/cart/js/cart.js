$(function () {

    $(".subShopping").click(function () {

        var current_btn = $(this);
        var cart_id = current_btn.parents("li").attr("cartid");
        console.log(cart_id);
        $.getJSON("/axf/subcart/", {"cartid": cart_id}, function (data) {
            console.log(data);

            if(data["status"] == "902"){
            //    数据彻底删除
                current_btn.parents("li").remove();
            }else if(data["status"] == "200"){
                var goods_num = data["goods_num"];
                current_btn.next().html(goods_num);
            }

        })

    })

    $(".addShopping").click(function () {

        var current_btn = $(this);
        var cart_id = current_btn.parents("li").attr("cartid");
        console.log(cart_id);
        $.getJSON("/axf/addcart/", {"cartid": cart_id}, function (data) {
            console.log(data);
            var goods_num = data["goods_num"];
            current_btn.prev().html(goods_num);
        })

    })

    $(".is_choose").click(function () {

        console.log("点击");
        var current = $(this);
        var cart_id = current.parents("li").attr("cartid");
        console.log(cart_id);

        $.getJSON("/axf/cartchangecheck/", {"cartid": cart_id}, function (data) {
            console.log(data);
            if (data["status"] == "200"){
                var is_select = data["is_select"];
                if (is_select){
                    current.find("span").html("√");
                }else{
                    current.find("span").html("");
                }
                current.attr("is_select", is_select);
                if (data["is_all_select"]){
                    $(".all_select").find("span").html("√");
                }else{
                    $(".all_select").find("span").html("");
                }
            }
        })

    })

    $(".all_select").click(function () {
        var selects = $(".is_choose");

        var select_list = [];
        // 记录所有没有选中
        var unselect_list = [];

        selects.each(function () {
            var is_select = $(this).attr("is_select");
            var cart_id = $(this).parents("li").attr("cartid");
            console.log(is_select);
            if (is_select.toLowerCase() == "false"){
                unselect_list.push(cart_id);
            }else{
                select_list.push(cart_id);
            }
        })

        if (unselect_list.length == 0){
            //   列表转换成一个数据 转换成一个字符串
            $.getJSON("/axf/allselect/",{"selects": select_list.join("#") }, function (data) {
                console.log(data);
                if(data["status"] == "200"){
                    var selects = data["selects"];

                    console.log(selects);

                    var select_list = selects.split("#");
                    console.log(select_list);
                    // for(var i = 0; i < select_list.length; i++){
                    //
                    // }
                    $(".is_choose").each(function () {
                        var current = $(this);
                        var cartid = $(this).parents("li").attr("cartid");
                        console.log(cartid);
                        for ( var i = 0; i < select_list.length; i++){
                            if (cartid == select_list[i]){
                                console.log("变更为未选中");
                                current.find("span").html("");
                                current.attr("is_select","false");
                            }
                        }
                        $(".all_select").find("span").html("");
                        // if (cartid in select_list){
                        //     console.log("在变更列表中");
                        //     $
                        // }else{
                        //     console.log("不在变更列表中");
                        // }
                    })
                }
            })
        }else{
            $.getJSON("/axf/allselects/", {"selects": unselect_list.join("#")}, function (data) {
                console.log(data);
                if( data["status"] == "200"){
                    var selects = data["selects"];
                    var select_list = selects.split("#");
                    for (var i=0; i< select_list.length; i++){
                       $(".is_choose").each(function () {
                           var is_choose = $(this);
                           var cartid = is_choose.parents("li").attr("cartid");
                           if(cartid == select_list[i]){
                               is_choose.find("span").html("√");

                               is_choose.attr("is_select","true");
                           }
                       })
                    }
                    $(".all_select").find("span").html("√");
                }
            })
        }


    })

    $("#generate_order").click(function () {

        var selects = [];

        $(".is_choose").each(function () {
            var current = $(this);
            if(current.attr("is_select").toLowerCase() == "true"){
                var select_id = current.parents("li").attr("cartid");
                selects.push(select_id);
            }
        })

        if (selects.length == 0){
            alert("您还没有选择任何商品");
        }else{
            $.getJSON("/axf/generateorder/", {"selects": selects.join("#")}, function (data) {
                console.log(data);
                if (data["status"] == "200"){
                    window.open("/axf/orderinfo/"+data["order_id"]+"/", target="_self");
                }
            })
        }
    })
})