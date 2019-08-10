var clothcount=0;
var key = "e94056233"
//收衣主頁
$(document).ready(()=>{
    $("#dryingmode").hide();
})
//button進入晾衣服頁面(晾衣服)
$("#dryingbtn").click(()=>{
    $.ajax({
        method:"get",
        url:"./drying?key="+key+",end="+false,
        success:(data)=>{
                    
        }
    })
    console.log("drying")
    $("#infoblock").hide();
    $("#dryingmode").show();
})
//button結束晾衣服
$("#enddrybtn").click(()=>{
    $("#dryingmode").hide();
    $("#infoblock").show();
    $("#clothcount").text(clothcount=0);
})
//button下一件衣服
$("#nextcloth").click(()=>{
    $("#clothcount").text(++clothcount);
    $.ajax({
        method:"get",
        url:"./drying?key="+key+"&end="+false,
        success:(data)=>{

        }

    })

})
