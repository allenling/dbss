$(document).ready(function(){
    $("label[for = 'id_context']").remove();
});

var timeclock = 1;

function join_or_quit(th_button){
    var card_id = th_button.attr("target");;
    var real_url = window.location.origin+"/action/"+th_button.attr("id")+"/";
    var t = real_url;
    $.ajax({
        type: "post",
        url: real_url,
        data: {"cid": th_button.attr("target")},
        success:function(data, textStatus){
          if (data["type"] == "redirect"){
            location.href=$("#toplogin").attr("href");
          }
          var warningpanel = $("#joins");
          warningpanel.text(data["type"]+":"+data["msg"]);
          warningpanel.css("text-align","center");
          warningpanel.show();
          tt();
        },
        error: function(xhr, textStatus, errorThrown){
          var warningpanel = $("#joine");
          warningpanel.text(errorThrown);
          warningpanel.show();
          tt();
        },
    });
}

function tt(){
  if (timeclock == 0){
  window.location.reload();
  }
  timeclock = timeclock -1;
  setTimeout("tt()", 1000);
}

$(".cardaction").click(function(){
    join_or_quit($(this));
});

//黑白名单
$(".listaction").click(function(){
  var rurl = window.location.href+$(this).attr("method");
  if ($(this).attr("method") == "black"){
    rurl = window.location.href+"blacklist";
  }else if($(this).attr("method") == "white"){
    rurl = window.location.href+"whitelist";
  }
  var fid=$(this).attr("id").split("_")[1];
  var action = $(this).attr("action");
  wblist(rurl, fid, action);
});

function wblist(rurl, fid, action){
    $.ajax({
        type: 'post',
        url: rurl, 
        data: {"fid":fid,"action":action},
        dataType:'ggjson',
        success:function(data, textStatus){
        },
        error:function(xhr, textStatus, errorThrown){
          alert(xhr+":  "+textStatus);
        }
    });
  
}
