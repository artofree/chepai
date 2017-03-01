var train_timer = 0;
var inputString = "";
var theTime = 0;
var firstRecord = 0;
var theImgUrl;
var theTimer;
var userName;
var testtimer;

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

function testtype() {
    clearInterval(testtimer);
    $.post(parms.setCode,
        {
            code: "123",
            times: "3000"
        },
        function (data, status) {
        });
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

$(document).ready(function () {
    initFrame();
    source = new EventSource("/getStatus");
    source.onmessage = function (event) {
        theList = event.data.split('-');
        if (theList[0] == '1') {
            $("#title").html('验证将在<mark id="countdown"></mark>秒后开始');
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
            testtimer = setInterval('testtype()', 3000);
        }
        if (theList[0] == '5') {
            $("#title").text('任务已结束，切勿刷新！请截图保存并私信发至群主');
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


//function getCodeImg() {
//    $.get(parms.getCodeImg, function (ret) {
//        theList = ret.split('-');
//        ///暂无验证
//        if (theList[0] == '0') {
//            setTimeout("getCodeImg()", 3000);
//        }
//        else if (theList[0] == '1') {
//            setTimeout("getCodeImg()", 200);
//        }
//        ///验证状态中
//        else if (theList[0] == '1') {
//            ///状态切换，开始倒计时
//            if (!isActive) {
//                isActive = 1;
//                $("#coreContent").html('<h2 id="train-img" style="width: 100%;color: black">验证将在<mark id="countdown"></mark>秒后开始</h2>');
//                $("#train-img").height(imgHeight);
//                $("#countdown").text(theList[1]);
//                setTimeout("getCodeImg()", 200);
//            }
//            else {
//                ///未上传验证图，继续倒计时
//                if (theList[2] == '') {
//                    $("#countdown").text(theList[1]);
//                    setTimeout("getCodeImg()", 200);
//                }
//                ///开始解码
//                else {
//                    var codeTimes = '';
//                    if (codetimes == 0) {
//                        codeTimes = '<h2 style="color: black">第一码：</h2>';
//                    }
//                    else {
//                        codeTimes = '<h2 style="color: black">第二码：</h2>';
//                    }
//
//                    $("#coreContent").html(codeTimes + '<img id="train-img" class="img-responsive" src="" style="width: 100%;margin-bottom: 10px">');
//                    $("#train-img").attr("src", theList[2]);
//                    $("#train-img").css({
//                        "display": "inline-block",
//                        "width": "400px",
//                        "height": "240px",
//                        "margin-bottom": "50px"
//                    });
//                    idt = theList[3];
//                    isWork = 1;
//                    codetimes += 1;
//                    var myDate = new Date();
//                    theTime = myDate.getTime();
//                    theTimer = setInterval('changeButton()', 1000);
//                }
//            }
//        }
//    })
//}


//$(document).ready(function () {
//    $("#train-input").keydown(function (event) {
//        if (event.which == '13') {
//            if (isWork) {
//                inputString = $("#train-input").val();
//                ///setCode
//                $.post(parms.setCode,
//                    {
//                        idt: idt,
//                        code: inputString
//                    },
//                    function (data, status) {
//                    });
//                var myDate = new Date();
//                if (codetimes == 1) {
//                    firstTime = (myDate.getTime() - theTime).toString();
//                    firstCode = inputString;
//                    train_timer = 0;
//                    clearInterval(theTimer);
//                    setTimeout("getCodeImg()", 200);
//                }
//                else {
//                    var theContent = (myDate.getTime() - theTime).toString();
//                    theContent = "<h3>你的第二码答案为：" + inputString + "</h3><br><strong>用时： " + theContent + " 毫秒</strong>";
//                    theContent = "<br><br><h3>你的第一码答案为：" + firstCode + "</h3><br><strong>用时： " + firstTime + " 毫秒</strong>" + theContent;
//                    $("#modalContent").html(theContent);
//                    $('#myModal').modal();
//                    $("#close_button").focus();
//                }
//            }
//        }
//    });
//});
