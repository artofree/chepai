var imgHeight = 0;
var isActive = 0;
var train_timer = 0;
var inputString = "";
var isWork = 0;
var theTime = 0;
var idt = 0;


function initFrame() {
    var theH = $(window).height();
    imgHeight = theH / 3;
    $("#train-img").height(imgHeight);
    var dlgMargin = (theH *4 /7).toString() + "px";
    $("#modalDlg").css("margin-top", dlgMargin);
    $("input").focus();
}

function changeButton() {
    train_timer += 1;
    $("#train-timer").text(train_timer.toString());
}

function getCodeImg() {
    $.get(parms.getCodeImg, function (ret) {
        theList = ret.split('-');
        ///暂无验证
        if (theList[0] == '0') {
            setTimeout("getCodeImg()", 5000);
        }
        ///验证状态中
        else if (theList[0] == '1') {
            ///状态切换，开始倒计时
            if (!isActive) {
                isActive = 1;
                $("#coreContent").html('<h2 id="train-img" style="width: 100%;color: black">验证将在<mark id="countdown"></mark>秒后开始</h2>');
                $("#train-img").height(imgHeight);
                $("#countdown").text(theList[1]);
                setTimeout("getCodeImg()", 200);
            }
            else {
                ///未上传验证图，继续倒计时
                if (theList[2] == '') {
                    $("#countdown").text(theList[1]);
                    setTimeout("getCodeImg()", 200);
                }
                ///开始解码
                else {
                    $("#coreContent").html('<img id="train-img" class="img-responsive" src="" style="width: 100%;margin-bottom: 10px">');
                    $("#train-img").attr("src", theList[2]);
                    $("#train-img").css({
                        "display": "inline-block",
                        "width": "400px",
                        "height": "240px",
                        "margin-bottom": "50px"
                    });
                    idt = theList[3];
                    isWork = 1;
                    var myDate = new Date();
                    theTime = myDate.getTime();
                    setInterval('changeButton()', 1000);
                }
            }
        }
    })
}

function initFun() {
    initFrame();
    getCodeImg();
}

$(document).ready(function () {
    initFun();
});

$(document).ready(function () {
    $("#train-input").keydown(function (event) {
        if (event.which == '13') {
            if (isWork) {
                inputString = $("#train-input").val();
                ///setCode
                $.post(parms.setCode,
                    {
                        idt: idt,
                        code: inputString
                    },
                    function (data, status) {
                    });
                var myDate = new Date();
                var theContent = (myDate.getTime() - theTime).toString();
                theContent = "<h3>你的答案为：" + inputString + "</h3><br><strong>用时： " + theContent + " 毫秒</strong>";
                $("#modalContent").html(theContent);
                $('#myModal').modal();
                $("#close_button").focus();
            }
        }
    });
});
