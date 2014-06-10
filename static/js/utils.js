function switch_spin(w){
  var sendspin = $("i#sendspin");
  var target_div = $("#friendslist");
  var  error_css = "fa fa-times fa-3x";
  var spin_css = "fa fa-spiner fa-spin fa-3x"
  if (sendspin.length == 0){
    var sendspin = $("<i ></i>");
    sendspin.addClass(spin_css);
    sendspin.attr("id","sendspin");
    target_div.css("text-align","center");
    target_div.append(sendspin);
  }
  if (w == "sendBefore"){
    if (sendspin.attr("class") != spin_css){
      sendspin.removeClass(error_css);
      sendspin.attr("class",spin_css);
    }
    sendspin.show();
  }else if(w == "success"){
    target_div.css("text-align","");
    sendspin.hide();
  }else if(w == "error"){
    if (sendspin.attr("class") != error_css){
      sendspin.removeClass(spin_css);
      sendspin.addClass(error_css);
      sendspin.show();
    }
  }

}

function get_usercss(id, imgstr, usernametsr, extra){
  switch_spin("success");
  var target_div = $("#friendslist");

  var out_div = $("<div ></div>");
  out_div.addClass(widthcon.userwall);
  out_div.addClass("userwall");
  out_div.attr("id","u_"+id);
  out_div.attr("target-name",usernametsr);
  var iner_userinfo = $("<div ></div>");
  iner_userinfo.addClass(widthcon.userinfo);
  iner_userinfo.addClass("userinfo");
  var imgavatar = $("<img >");
  imgavatar.attr("src",imgstr);
  imgavatar.attr("width","50");
  imgavatar.attr("height","50");
  iner_userinfo.append(imgavatar);
  var iner_other = $("<div ></div>");
  iner_other.addClass(widthcon.useraction);
  iner_other.addClass("useraction");
  iner_other.css("padding-left","0");
  iner_other.css("padding-right","0");
  var other_username = $("<p ></p>");
  if (extra != undefined ){
  var other_something = addactiontext(id, out_div, extra);
  }else{
  var other_something = addactiontext(id, out_div);
  }

  other_username.text(usernametsr);
  iner_other.append(other_username);
  iner_other.append(other_something);

  out_div.append(iner_userinfo);
  out_div.append(iner_other);
  target_div.append(out_div);
 
}

function error_handler(textStatus, errorThrown){
  switch_spin("error");
  var target_div = $("#friendslist");
  target_div.append(textStatus);
  target_div.append(errorThrown);
}

function takefriends(rurl, extra){
    $.ajax({
        type: "get",
        url: rurl,
        beforeSend: function(XmlHttpRequest){
            switch_spin("sendBefore");
        },
        success:function(data, textStatus){
            var result_json = data['results'];
            for(i in result_json){
            if (extra != undefined ){
               get_usercss(result_json[i]['id'], result_json[i]['avatar_set'], result_json[i]['username'], result_json[i][extra]);
            }else{
               get_usercss(result_json[i]['id'], result_json[i]['avatar_set'], result_json[i]['username']);
            }
            }
        },
        error: function(xhr, textStatus, errorThrown){
            error_handler(textStatus, errorThrown);
        }
    });
}
