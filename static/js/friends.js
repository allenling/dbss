
function friendaction(tuid){
    var rurl = window.location.origin+"/action/";
    var tspan = $("span#check_"+tuid);
    var tspanminus = tspan.children("i.fa.fa-minus-circle");
    var tspanplus = tspan.children("i.fa.fa-plus-circle");

    if (tspanminus.length > 0){
        rurl = rurl + "removeconcern/";
    }else if (tspanplus.length > 0){
        rurl = rurl + "addconcern/";
    }else{
      return false;
    }
    var tuserspan = tspan.children("i.fa.fa-users");
    var bookmark = tspan.children("i.fa.fa-bookmark");
    $.ajax({
        type: 'post',
        url: rurl, 
        data: {"tuid": tuid},
        dataType:'json',
        success: function(data, textStatus){
          if (data["type"] == "redirect"){
            location.href=$("#toplogin").attr("href");
          }
        success_or_error(1, data["type"], data["msg"]);
        if (tspanminus.length > 0){
            if (data["extra"] == "bookmark"){
                 tuserspan.removeClass("fa fa-users");
                 tuserspan.addClass("fa fa-bookmark");
            }
            tspanminus.removeClass("fa fa-minus-circle");
            tspanminus.addClass("fa fa-plus-circle");
        }else if (tspanplus.length > 0){
            if (data["extra"] == "users"){
                bookmark.removeClass("fa fa-bookmark");
                bookmark.addClass("fa fa-users");
            }
            tspanplus.removeClass("fa fa-plus-circle");
            tspanplus.addClass("fa fa-minus-circle");
        }
        },
        error: function(xhr, textStatus, errorThrown){
            success_or_error(0, textStatus, errorThrown);
        }
    });
}

function success_or_error(action, type, msg){
    var tar = $("#panetar");
    var rspan = $("#joins");
    var repan = $("#joine");
  if (action == 1){
          if (repan.length != 0){
            repan.css("display","none");
          }
          if (rspan.length ==0){
            rspan = initspanel();
            tar.before(rspan);
          }else{
            rspan.css("display","");
          }
          rspan.children("button").after(type+":"+msg);
  }else if (action == 0){
          if (rspan.length != 0){
            rspan.css("display","none");
          }
          if (repan.length !=0){
            repan = initepanel();
            tar.before(repan);
          }else{
            repan.css("display","");
          }
          repan.children("button").after(type+":"+msg);
  }
}

function initspanel(){
  var outp = $("<div ></div>");
  outp.addClass("alert alert-success");
  outp.attr("id","joins");
  outp.attr("data-dismiss","alert");
  var inbutton = $("<button ></button>");
  inbutton.attr("type", "button");
  inbutton.addClass("close");
  inbutton.attr("data-dismiss", "alert");
  inbutton.attr("aria-hidden","true");
  var initag = $("<i ></i>");
  initag.addClass("fa fa-times");
  inbutton.append(initag);
  outp.append(inbutton);
  return outp;
}

function initepanel(){
  var outp = initspanel();
  outp.removeClass("alert alert-success");
  outp.addClass("alert alert-warning");
  outp.attr("id","joine");
  var inbutton = $("<button ></button>");
  inbutton.attr("type", "button");
  inbutton.addClass("close");
  inbutton.attr("data-dismiss", "alert");
  inbutton.attr("aria-hidden","true");
  var initag = $("<i ></i>");
  initag.addClass("fa fa-times");
  inbutton.append(initag);
  outp.append(inbutton);
  return outp;
}
