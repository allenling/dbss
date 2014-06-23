function setfcardcss(data){
  var contextdiv = $("#fcards");
  var tmpmain = $("#fcardtemp");
  for (var i = 0; i< data.length; i++){
    var tmpcard = tmpmain.clone(true);
    var tmpdate = tmpcard.find("small#tmpdate");
    tmpdate.text(data[i]["pub_date"].substring(0,19));
    var tmpcontext = tmpcard.find("div#tmpcontext");
    tmpcontext.html(data[i]["context"]);
    tmpcontext.removeAttr("id");
    tmpdate.removeAttr("id");
    tmpcard.removeAttr("id");
    tmpcard.show();
    contextdiv.append(tmpcard);
  }
}

//
function rearrow(di, aurl){
      var fili = $("<li ></li>");
      var filia = $("<a ></a>");
      var filiai = $("<i></i>");
      filiai.addClass("fa fa-arrow-circle-"+di);
  filia.attr("href",aurl);
      filia.append(filiai);
      fili.append(filia);
  return fili;
}

function repali(tnum, turl, isnow){
      var tli = $("<li ></li>");
      var tli_a = $("<a ></a>");
      tli_a.attr("target",turl)
      tli_a.text(tnum);
  if (isnow){
    tli.addClass("active");
  }
     tli.bind("click",function(){
       getdatajax($(this).attr("target"), 'Detail');
     });
     tli.append(tli_a);
  return tli;

}

function redotpa(){
  var dotli = $("<li></li>");
  var dotlia = $("<a></a>");
  dotli.addClass("disable");
  dotli.append(dotlia);
  return dotli;
}

//js pagination
function setpagin(mcounts, prev, next, len){
  var counts = 1;
  if (next != null){
    counts = Math.ceil(mcounts/len);
  }else if(prev != null){
    var nowp = parseInt(prev.split("?page=")[1])+1;
  }
  var targetdiv = $("#fcards");
  var pul = $("<ul ></ul>");
  pul.addClass("pagination");
  var tempv = false;

  if (prev == null && next == null ){
      pul.append(repali(1, "", true));
      targetdiv.append(pul);
      return false;
  }

  if (prev != null){
  var pagea = prev.substring(0,prev.indexOf("=")+1);
    var nowp = parseInt(prev.split("?page=")[1])+1;
    var st = 1;
    if (nowp-1>5){
      pul.append(rearrow("left"), pagea+(nowp+1));
      pul.append(repali(1, pagea+"1"));
      pul.append(redotpa());
      st = nowp;
    }
    for (var i =st; i<nowp;i++){
      pul.append(repali(i, pagea+i));
    }
      pul.append(repali(nowp, pagea+nowp, true));
  }else{
    var pagea = next.substring(0,next.indexOf("=")+1);
    pul.append(repali(1, pagea+"1", true));
    tempv = true;
  }
  if(next != null){
    var pagea = next.substring(0,next.indexOf("=")+1);
    var nowp = parseInt(next.split("?page=")[1])-1;
    if(counts-nowp > 5){
      for (var j = 1;j<5;j++){
        var tturl = pagea+(nowp+j);
        pul.append(repali((nowp+j),pagea+(nowp+j)));
      }
      pul.append(redotpa());
      pul.append(repali(counts, pagea+counts));
      pul.append(rearrow("right", pagea+(nowp+1)));
    }else{
      for (var j = nowp+1;j <=counts;j++){
        pul.append(repali(j,pagea+j));
      }
    }
  }
  targetdiv.append(pul);

}

function getcardata(yeard, monthd, dayd){
  var sog = $(".sog.active");
  var options = sog.attr("target");
  var tmpurl = window.location.href;

  if (yeard != undefined){
    if (monthd != undefined){
      if (dayd != undefined){
      var rurl = tmpurl+"year/"+yeard+"/month/"+monthd+"/day/"+dayd;
      }else{
      var rurl = tmpurl+"year/"+yeard+"/month/"+monthd;
      }
    }else{
      var rurl = tmpurl+"year/"+yeard;
    }
  }else{
    alert("error: no params!");
    return false;
  }
  if (options == "Graphic"){
    rurl = rurl+'/graphic/'
  }
  getdatajax(rurl, options);

}

function getdatajax(turl, options){
    $.ajax({
        type: "get",
        url: turl,
        beforeSend: function(XmlHttpRequest){
        var bfsend = $("#bfsenda");
        bfsend.show();
        },
        success:function(data, textStatus){
        var bfsend = $("#bfsenda");
        bfsend.hide();
        if(options == "Detail"){
            var contextdiv = $("#fcards");
            contextdiv.empty();
            setfcardcss(data['results']);
            setpagin(data['count'],data['previous'],data['next'], data['results'].length);
        }else if(options == "Graphic"){
          showgraphic(data);
        }
        },
        error: function(xhr, textStatus, errorThrown){
          alert(textStatus+":"+errorThrown);
                 var x = $("#bfsend");
                 x.css("display","none");
           // error_handler(textStatus, errorThrown);
        }
    });
}



$("#timeline").click(function (){
    $("#subtimeline").fadeToggle();
    var turl = window.location.href;
    var rurl = turl + 'graphic/';
    $.ajax({
        type: "get",
        url: rurl,
        success:function(data, textStatus){
          var rdata = JSON.parse(data);
          var targetul = $("#subtimelineul");
          targetul.empty();
          for (var i in rdata){
            var yearli = $("<li></li>");
            yearli.attr("target",i);
            yearli.addClass("ftimeli");
            var yeara = $("<a ></a>");
            yeara.addClass("subyear");
            yeara.text(i+"年");
            yearli.append(yeara);
            yearli.bind("click", function(){
                  var sog = $(".sog.active");
                  if (sog.length == 0){
                      alert("please select one condition, Detail or Graphic!");
                  }else {
                      var tmp = $(".ftimeli.active").removeClass("active");
                      $(this).addClass("active");
                      getcardata($(this).attr("target"));
                  }

            });
            targetul.append(yearli);
            var rsubdata = JSON.parse(rdata[i]);
            for (var j in rsubdata){
              var submonth = $("<li></li>");
              submonth.attr("target",i+"_"+j);
              submonth.addClass("ftimeli");
              var submontha = $("<a ></a>");
              submontha.addClass("submonth");
              submontha.text(j+"月");
              submontha.css("padding-left","30px");
              submonth.append(submontha);
              targetul.append(submonth);
              submonth.bind("click",function (){
                  var sog = $(".sog.active");
                  if (sog.length == 0){
                      alert("please select one condition, Detail or Graphic!");
                      return false;
                  }else {
                         var tmp = $(".ftimeli.active");
                         tmp.removeClass("active");
                         $(this).addClass("active");
                        var ddata = $(this).attr("target").split("_");
                        var yyear = ddata[0];
                        var mmonth = ddata[1];
                        getcardata(yyear, mmonth);
                  }
              });
              for (var z in rsubdata[j]){
              var subday = $("<li></li>");
              subday.attr("target",i+"_"+j+"_"+rsubdata[j][z]);
              subday.addClass("ftimeli");
              var subdaya = $("<a ></a>");
              subdaya.addClass("subday");
              subdaya.text(rsubdata[j][z]+"日");
              subdaya.css("padding-left","40px");
              subday.append(subdaya);
              targetul.append(subday);
              subday.bind("click",function (){
                  var sog = $(".sog.active");
                  if (sog.length == 0){
                      alert("please select one condition, Detail or Graphic!");
                  }else {
                         var tmp = $(".ftimeli.active");
                         tmp.removeClass("active");
                         $(this).addClass("active");
                         var ddata = $(this).attr("target").split("_");
                        var yyear = ddata[0];
                        var mmonth = ddata[1];
                        var dday  = ddata[2];
                        getcardata(yyear, mmonth, dday);
                  }
                  });
              }
            }
          }
        }
    });
});

function revalist(data){
  var tvalist = [];
  var tmp = $(".ftimeli.active");
  var when = tmp.attr("target");
  var datetitle = when.split("_");
  var mtitle=$("#modaltitle");
  if (when.split("_").length == 3){
    //year, month, day
    mtitle.text(datetitle[0]+"年"+datetitle[1]+"月"+datetitle[2]+"日");
    var dcount = 1;
    for (var i in data){
      tvalist.push({"datetime":data[i],"value":dcount});
      dcount = dcount + 1;
    }
  }else if(when.split("_").length == 2){
    //year, month
    mtitle.text(datetitle[0]+"年"+datetitle[1]+"月");
    for (var i in data){
      tvalist.push({"datetime":i+"日","value":data[i]});
    }
  }else{
    //year
    mtitle.text(when+"年");
    for (var i in data){
      var m = i.split("_")[1];
      tvalist.push({"datetime":m+"月","value":data[i]});
    }
  }
  return tvalist;
}

function showgraphic(data){
  var rdata = JSON.parse(data);
  if (typeof(rdata) == "string"){
    rdata = JSON.parse(rdata);
  }
  $("#myg").show();
  $("#myg").empty();
  var valuelist = revalist(rdata);
  /**
  var targetd = $("<div ></div>");
  $("#mbody").empty();
  targetd.attr("id","myg");
  targetd.css("height","300px");
  $("#mbody").append(targetd);
  **/

 var tmpparam={
   element: "myg",
   data:valuelist,
   xkey:"datetime",
   ykeys:["value"],
   labels:["次数"],
   parseTime:false
 };
  new Morris.Line(tmpparam);
}

$(".sog").click(function(){
   $(".sog.active").removeClass("active");
  $(this).addClass("active"); 
});
