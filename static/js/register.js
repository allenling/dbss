$(document).ready(function(){

	/** user input css **/
    var inputgroup1 = $("<div ></div>");
    inputgroup1.addClass("input-group");
    var useraddon = $("<span ></span>");
    useraddon.addClass("input-group-addon");
    var fauser = $("<i></i>").addClass("fa");
    fauser.addClass("fa-user");
    fauser.addClass("fa-lg");
    useraddon.append(fauser);
    $("#id_base-username").addClass("form-control");
    if($("#id_base-username").css("value") === undefined){
	    $("#id_base-username").attr("placeholder","用户名");
    }
    inputgroup1.append(useraddon);
    inputgroup1.append($("input#id_base-username"));
    $("[for = 'id_base-username']").after(inputgroup1);

    /** email input css **/
    var inputgroup2 = $("<div ></div>");
    inputgroup2.addClass("input-group");
    var emailaddon = $("<span ></span>");
    emailaddon.addClass("input-group-addon");
    var faenvelope = $("<i></i>").addClass("fa");
    faenvelope.addClass("fa-envelope");
    emailaddon.append(faenvelope);
    $("#id_base-email").addClass("form-control");
    if($("#id_base-email").css("value") === undefined){
	    $("#id_base-email").attr("placeholder","邮件地址");
    }
    inputgroup2.append(emailaddon);
    inputgroup2.append($("input#id_base-email"));
    $("[for = 'id_base-email']").after(inputgroup2);

    /** passwordcom css **/
    var inputgroup3 = $("<div ></div>");
    inputgroup3.addClass("input-group");
    var passwordaddon = $("<span ></span>");
    passwordaddon.addClass("input-group-addon");
    var fakey = $("<i></i>").addClass("fa");
    fakey.addClass("fa-key");
    passwordaddon.append(fakey);
    $("#id_base-password").addClass("form-control");
    if($("#id_base-password").css("value") === undefined){
	    $("#id_base-password").attr("placeholder","密码");
    }
    inputgroup3.append(passwordaddon);
    inputgroup3.append($("input#id_base-password"));
    $("[for = 'id_base-password']").after(inputgroup3);

    /** passwordcom css **/
    var inputgroup4 = $("<div ></div>");
    inputgroup4.addClass("input-group");
    var passwordcomaddon = $("<span ></span>");
    passwordcomaddon.addClass("input-group-addon");
    var falock = $("<i></i>").addClass("fa");
    falock.addClass("fa-lock");
    falock.addClass("fa-lg");
    falock.css("width","14px");
    passwordcomaddon.append(falock);
    $("#id_base-passwordcom").addClass("form-control");
    if($("#id_base-passwordcom").css("value") === undefined){
	    $("#id_base-passwordcom").attr("placeholder","确认密码");
    }
    inputgroup4.append(passwordcomaddon);
    inputgroup4.append($("input#id_base-passwordcom"));
    $("[for = 'id_base-passwordcom']").after(inputgroup4);




    /** register2 css **/
    var capdiv = $("<div ></div>");
    capdiv.addClass("col-sm-2");
    capdiv.append($("img.captcha"));
    $("[for = 'id_captcha-captcha_1']").after(capdiv);

    var captchainputdiv = $("<div ></div>");
    captchainputdiv.addClass("col-sm-6");
    var divinput = $("input#id_captcha-captcha_1");
    divinput.addClass("form-control");
    captchainputdiv.append(divinput);
    $("input#id_captcha-captcha_0").after(captchainputdiv);
});
