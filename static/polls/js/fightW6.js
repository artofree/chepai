var train_timer = 0;
var inputString = "";
var theTime = 0;
var firstRecord = 0;
var theImgUrl;
var theTimer;
var userName;
var heartbeatTime =0;
var heartbeatTimer;
//var testtimer;

function checkHeartBeat(){
    var myDate = new Date();
    //如果每次计时的5秒间隔里没有来心跳，提示刷新
    if (myDate.getTime() -heartbeatTime >5000){
        $("#title").html('连接已断开，请刷新!');
        clearInterval(heartbeatTimer);
    }
}

function GetRandomNum(Min, Max) {
    var Range = Max - Min;
    var Rand = Math.random();
    return (Min + Math.round(Rand * Range));
}

var testCode = ['2345', '1234', '3465'];

//$(document).ready(function () {
//    if ( $.browser.webkit ) {
//        $("#title").html('chrome');
//    }
//});

function initFrame() {
    var theH = $(window).height();
    var dlgMargin = (theH * 4 / 7).toString() + "px";
    $("#modalDlg").css("margin-top", dlgMargin);
}

function changeButton() {
    train_timer += 1;
    $("#train-timer").text(train_timer.toString());
}

//function testtype() {
//    clearInterval(testtimer);
//    $.post(parms.setCode,
//        {
//            code: "123",
//            times: "2000"
//        },
//        function (data, status) {
//        });
//}

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

$(document).ready(function () {
    initFrame();
    source = new EventSource("/getStatus");
    source.onmessage = function (event) {
        theList = event.data.split('-');
        if (theList[0] == '0') {
            if(theList[1] =='ok'){
                $("#title").html('已成功建立连接,暂无任务进行');
                var myDate = new Date();
                heartbeatTime = myDate.getTime();
                heartbeatTimer = setInterval('checkHeartBeat()', 5000);
            }
            if(theList[1] =='heartbeat'){
                var myDate = new Date();
                heartbeatTime = myDate.getTime();
            }
        }
        if (theList[0] == '1') {
            $("#title").html('任务将在<mark id="countdown"></mark>秒后开始');
            $("#countdown").text(theList[1]);
        }
        if (theList[0] == '2') {
            $("#countdown").text(theList[1]);
            if (theList.length == 3) {
                $("#theImg").attr("src", theList[2]);
                $("#which").text('预览码 :');
            }
            else {
                $("#which").text('');
                //$("#theImg").attr("src", '');
                $("#theImg").removeAttr('src');
            }
        }
        if (theList[0] == '3' || theList[0] == '4') {
            $("#theImg").attr("src", theList[1]);
            if (theList[0] == '3') {
                $("#title").text('第一码 :');
            }
            if (theList[0] == '4') {
                $("#title").text('第二码 :');
                if (!firstRecord) {
                    record(1);
                    firstRecord = 1;
                }
            }
            theImgUrl = theList[1];
            $("#theInput").val('');
            $("#theInput").removeAttr("disabled");
            $("input").focus();
            var myDate = new Date();
            theTime = myDate.getTime();
            clearInterval(theTimer);
            train_timer = 0;
            $("#train-timer").text(train_timer.toString());
            theTimer = setInterval('changeButton()', 1000);
            //testtimer = setInterval('testtype()', 2000);
        }
        if (theList[0] == '5') {
            $("#title").text('任务已结束，切勿刷新！请截图保存并私信发至群主');
            clearInterval(heartbeatTimer);
        }
    };
});

$(document).ready(function () {
    $.get(parms.getusrname, function (ret) {
        $("#usrname").text(ret);
        userName = ret;
    });
    $("#theInput").keydown(function (event) {
        if (event.which == '13') {
            inputString = $("#theInput").val();
            if (inputString != '') {
                ///setCode
                var myDate = new Date();
                during = (myDate.getTime() - theTime).toString();
                $.post(parms.setCode,
                    {
                        code: inputString,
                        //code: testCode[GetRandomNum(0 ,2)],
                        times: during
                    },
                    function (data, status) {
                    });
                ///清理
                $("#which").text('');
                $("#theImg").removeAttr('src');
                train_timer = 0;
                $("#train-timer").text(train_timer.toString());
                clearInterval(theTimer);
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
