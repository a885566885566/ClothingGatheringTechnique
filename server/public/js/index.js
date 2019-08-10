var clothcount=0;
var key = "e94056233"
var CLOTH_STATE = ['EMPTY', 'WET', 'DRY']
var drying_flag = false
//收衣主頁
$(document).ready(()=>{
    var update_state = ()=>{
        $.ajax({
            method:"get",
            url:"../status",
            success:(batches)=>{
                batches.forEach((batch)=>{
                    console.log(batch)
                    var item = $('<div class="status_item"><div class="cloth_num"><p class="big_number" id="cloth_num_'+batch["batch"]+'">'+batch["num"]+'</p><p>件</p></div><div><div class="cloth_state"><p>目前狀態:</p><p id="cloth_state">'+CLOTH_STATE[batch["status"]]+'</p></div> <div class="cloth_state"><p>晾衣時間:</p><p id="cloth_time">'+batch["time"]+'</p></div><button type="button" class="btn btn-success" id="cloth_btn">我要收衣服!</button></div></div>')
                    item.appendTo($('#status_list'))
                })
            }
        })
    }

    var pollingDrying = ()=>{
        $.ajax({
            method:"get",
            url:"../drying?key="+key+"&end=0",
            success:(data)=>{
                if(data["status"]=="ok"){
                    $('#btn_next_cloth').attr("disabled");
                }
                else{
                    $('#btn_next_cloth').removeAttr("disabled");
                    setTimeout(pollingDrying, 1000);
                }
            }
        })
    }
    $("#mode_drying").hide();
    update_state()

    $("#btn_drying").click(()=>{
        $("#mode_status").hide();
        $("#mode_drying").show();
    })
    //button結束晾衣服
    $("#enddrybtn").click(()=>{
        $("#mode_drying").hide();
        $("#infoblock").show();
        $("#clothcount").text(clothcount=0);
    })
    //button下一件衣服
    $("#btn_next_cloth").click(()=>{
        console.log("drying")
        pollingDrying()
    })
})
//button進入晾衣服頁面(晾衣服)

