var train_timer = 0;
var inputString = "";
var theTime = 0;
var firstRecord = 0;
var theImgUrl;
var buttonTimer;
var countTimer;

var countNum = 20;
var yulanTime = 12;
var yulanEndTime = 1;
var firstDuring = 6000;
var drillList;


function changeButton() {
    train_timer += 1;
    $("#train-timer").text(train_timer.toString());
}

function record(times, during, thecode) {
    ///向下记录
    if (times == 1) {
        $("#code1").text(thecode);
        $("#time1").text(during);
        $("#img1").attr("src", theImgUrl);
    }
    else {
        $("#code2").text(thecode);
        $("#time2").text(during);
        $("#img2").attr("src", theImgUrl);
    }
}

function showSecondCode() {
    ///如果第一码没有keydown
    if (!firstRecord) {
        record(1,'','');
        firstRecord = 1;
        clearInterval(buttonTimer);
    }
    $("#title").text('第二码 :');
    theImgUrl ="/static/exp/" + drillList[2] + ".png";
    $("#theImg").attr("src",theImgUrl);
    $("#theInput").removeAttr("disabled");
    $("input").focus();
    var myDate = new Date();
    theTime = myDate.getTime();
    train_timer = 0;
    $("#train-timer").text(train_timer.toString());
    buttonTimer = setInterval('changeButton()', 1000);
}

function showFirstCode() {
    $("#title").text('第一码 :');
    theImgUrl ="/static/exp/" + drillList[1] + ".png";
    $("#theImg").attr("src", theImgUrl);
    $("#theInput").removeAttr("disabled");
    $("input").focus();
    var myDate = new Date();
    theTime = myDate.getTime();
    $("#train-timer").text(train_timer.toString());
    buttonTimer = setInterval('changeButton()', 1000);
    setTimeout("showSecondCode()", firstDuring);
}

function countDown() {
    countNum -= 1;
    $("#countdown").text(countNum.toString());
    if (countNum == yulanTime) {
        $("#theImg").attr("src", "/static/exp/" + drillList[0] + ".png");
        $("#which").text('预览码 :');
    }
    if (countNum == yulanEndTime) {
        $("#which").text('');
        $("#theImg").removeAttr('src');
    }
    if (countNum == 1) {
        clearInterval(countTimer);
        setTimeout("showFirstCode()", 3000);
    }
}

$(document).ready(function () {
    $.get(parms.getDrillInfo, function (ret) {
        drillList = ret.split('-');
        $("#title").html('验证将在<mark id="countdown"></mark>秒后开始');
        $("#countdown").text(countNum.toString());
        countTimer = setInterval('countDown()', 1000);
    })
});

$(document).ready(function () {
    $("#theInput").keydown(function (event) {
        if (event.which == '13') {
            inputString = $("#theInput").val();
            if (inputString != '') {
                var myDate = new Date();
                during = (myDate.getTime() - theTime).toString();
                ///清理
                $("#which").text('');
                train_timer = 0;
                $("#train-timer").text(train_timer.toString());
                clearInterval(buttonTimer);
                $("#theInput").val('');
                $("#theInput").attr("disabled", 'disabled');
                ///记录
                if (!firstRecord) {
                    record(1, during, inputString);
                    firstRecord = 1;
                }
                else {
                    record(2, during, inputString);
                }
            }
        }
    });
});
