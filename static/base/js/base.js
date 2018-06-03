$(document).ready(function(){
    document.documentElement.style.fontSize = innerWidth / 10 + "px";

    var url = location.href;
    //  http://127.0.0.1:8000/home/
    var spanId = url.split("/")[3];
    var $span = $(document.getElementById(spanId))

    $span.css("background", "url(/static/base/img/"+spanId+"1.png) no-repeat")
    $span.css("background-size", "0.6rem")
})