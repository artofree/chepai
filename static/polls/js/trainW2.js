var second = 1000;
var train_timer = 0;
var inputString = "";
var theCode = "";
var theTime = 0;
var totalCorect = 0;
var totalTimes =0;

function changeButton() {
    train_timer += 1;
    $("#train-timer").text(train_timer.toString());
}

function initFrame() {
    $.get(parms.getusrname, function (ret) {
        $("#usrname").text(ret);
    });
    var theH = $(window).height();
    var dlgMargin = (theH * 3 / 7).toString() + "px";
    //$("#modalDlg").css("margin-top", dlgMargin);
    $("#modalDlg").css("margin-top", "360px");
    $("input").focus();
}

function getPhoto() {
    $.get(parms.photoUrl, function (ret) {
        theList = ret.split('-');
        theCode = theList[1];
        $("#train-img").attr("src", "/static/exp/" + theList[0] + ".png");
        var myDate = new Date();
        theTime = myDate.getTime();
    })
}

function initFun() {
    initFrame();
    setInterval('changeButton()', second);
    getPhoto();
}

$(document).ready(function () {
    initFun();
});

$(document).ready(function () {
    $("input").keydown(function (event) {
        if (event.which == '13') {
            inputString = $("#train-input").val();
            var myDate = new Date();
            var theContent = (myDate.getTime() - theTime).toString();
            totalTimes +=1;
            if (inputString == theCode) {
                theContent = "<h1>答案正确!</h1><br><strong>用时： " + theContent + " 毫秒</strong><br>";
                if (myDate.getTime() - theTime < 5000) {
                    totalCorect += 1;
                    if (totalCorect == 50) {
                        $.post(parms.finjob,
                            {
                                total: totalTimes
                            },
                            function (data, status) {
                            });
                    }
                }
            }
            else {
                theContent = "<h1>答案错误！</h1><br><strong>正确答案为 ：" + theCode + "</strong><br>";
            }
            theContent += "<h1>总码数 : <strong>" + totalTimes.toString() + "</strong></h1>";
            theContent += "<h1>有效码 : <strong>" + totalCorect.toString() + "</strong></h1>";
            $("#modalContent").html(theContent);
            $('#myModal').modal();
            $("#close_button").focus();
        }
    });
});

$(document).ready(function () {
    $("#myModal").keydown(function (event) {
        if (event.which == '13') {
            $('#myModal').modal('hide')
        }
    });
});

$('#myModal').on('hidden.bs.modal', function (e) {
    getPhoto();
    $("#train-input").val("");
    train_timer = 0;
    $("#train-timer").text("0");
    inputString = "";
    $("input").focus();
});