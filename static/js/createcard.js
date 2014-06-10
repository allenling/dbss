$(document).ready(function(){
    //title css
    var inputgroup_t = $("<div ></div>");
    inputgroup_t.addClass("form-group");
    $("#id_title").addClass("form-control");
    $("#id_title").attr("placeholder","活动标题!");
    inputgroup_t.append($("#id_title"));
    $("[for = 'id_title']").after(inputgroup_t);
    $("[for = 'id_title']").remove();
    inputgroup_t.css("margin-bottom","30px");

    $("[for = 'id_context']").remove();
    $("[for = 'id_property']").html("Public: 公开的活动，每个人都可以查看，加入你的活动卡<br > Private: 只有你邀请的好友可以查看活动卡，并且只有该活动卡的成员才能收到该活动的更新");
    $("[for = id_property]").css("margin-top","30px");

    $("#id_property").addClass("form-control");
    $("#id_property").css("margin-bottom","20px");

    $(".bootstrap-tagsinput").css("width","150%");
    $(".bootstrap-tagsinput").css("line-height","40px");

});
