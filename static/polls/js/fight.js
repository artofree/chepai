var imgHeight = 0;
var isActive = 0;
var train_timer = 0;
var inputString = "";
var isWork = 0;
var theTimer = 0;
var idt =0;


function initFrame() {
    var theH = $(window).height();
    imgHeight = theH / 3;
    $("#train-img").height(imgHeight);
    $(".num").height((theH - theH / 3 - 105) / 4);
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
            ///状态切换
            if (!isActive) {
                isActive = 1;
                $("#coreContent").html('<h2 id="train-img" style="width: 100%;color: black">验证将在<mark id="countdown"></mark>秒后开始</h2>');
                $("#train-img").height(imgHeight);
                $("#countdown").text(theList[1]);
                setTimeout("getCodeImg()", 200);
            }
            else {
                if (theList[2] == '') {
                    $("#countdown").text(theList[1]);
                    setTimeout("getCodeImg()", 200);
                }
                else {
                    $("#coreContent").html('<img id="train-img" class="img-responsive" src="" style="width: 100%;margin-bottom: 10px">');
                    $("#train-img").height(imgHeight);
                    $("#train-img").attr("src", theList[2]);
                    idt =theList[3];
                    isWork = 1;
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


$(document).bind('touchmove', function (event) {
    event.preventDefault();
});

$(document).bind('touchstart', function (event) {
    var tar = event.originalEvent.targetTouches[0].target;
    if (tar.id != 'close_button') {
        if (isWork) {
            if (tar.id != 'train-timer' && tar.nodeName == 'BUTTON') {
                var content = tar.innerText;
                if (content == "<-") {
                    inputString = inputString.substring(0, inputString.length - 1);
                    $("#train-input").text(inputString);
                }
                else if (content.length > 1) {
                    inputString = $("#train-input").text();
                    ///setCode
                    $.post(parms.setCode,
                        {
                            idt: idt,
                            code: inputString
                        },
                        function (data, status) {
                        });
                }
                else {
                    inputString += content;
                    $("#train-input").text(inputString);
                }
            }
        }
    }
    event.preventDefault();
});

//$(document).bind('click', function (event) {
//    var tar = event.target;
//    if (tar.id != 'close_button') {
//        if (isWork) {
//            if (tar.id != 'train-timer' && tar.nodeName == 'BUTTON') {
//                var content = tar.innerText;
//                if (content == "<-") {
//                    inputString = inputString.substring(0, inputString.length - 1);
//                    $("#train-input").text(inputString);
//                }
//                else if (content.length > 1) {
//                    inputString = $("#train-input").text();
//                    ///setCode
//                    $.post(parms.setCode,
//                        {
//                            idt: idt,
//                            code: inputString
//                        },
//                        function (data, status) {
//                        });
//                }
//                else {
//                    inputString += content;
//                    $("#train-input").text(inputString);
//                }
//            }
//        }
//    }
//});