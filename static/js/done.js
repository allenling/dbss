$(document).ready(function(){
    var second = $("#totalSecond").text();
  setInterval(redirect, 1000);
  function redirect(){
    if (second < 0){
      location.href=$("#tarp").attr("target-url");
    }else{
    $("#totalSecond").text(second--);
    }
  }
});
