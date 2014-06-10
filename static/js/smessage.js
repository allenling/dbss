widthcon = {"userwall":"col-sm-4", "userinfo":"col-sm-4","useraction":"col-sm-8"}

$(document).ready(function(){
    $("#id_towho").bind("itemRemoved",function(data){
      var targetname = data.item;
      var targetuser = $("span[target-name="+targetname+"]");
      if (targetuser.length != 0){
      targetuser.text("选择");
      }
    });
    $(".bootstrap-tagsinput").css("width","inherit");
    $(".bootstrap-tagsinput").css("line-height","30px");
});


function addactiontext(id, out_div){
  var other_something = $("<p ></p>");
    var c_button = $("<span ></span>");
    c_button.attr("type", "button");
    c_button.attr("target",id);
    c_button.attr("target-name", out_div.attr("target-name"));
    c_button.addClass("label label-warning");
    c_button.attr("id","check_"+id);
    var inornot = $("#id_towho").val();
    var tname = out_div.attr("target-name");
    if(inornot == "" || (inornot.indexOf(tname) == -1 && inornot.indexOf(tname+",") == -1)){
      c_button.text("选择");
    }else{
      c_button.text("取消");
    }
  var cornot = out_div.text();
    c_button.bind("click", function(){
  if ($(this).text() == "选择"){
    $(this).text("取消");
  $("#id_towho").tagsinput("add", $(this).attr("target-name"));
  }else{
    $(this).text("选择");
  $("#id_towho").tagsinput("remove", $(this).attr("target-name"));
  }
    });
   other_something.append(c_button);
  return other_something;
}


$("#sfriends").click(function(){
  var flist = $("#friendslist");
  flist.empty();
  var rurl = $(this).attr("target-url");
  takefriends(rurl);
});
