var second = 1000;
var train_timer = 0;
var inputString = "";
var theCode = "";
var theTime = 0;

function changeButton() {
    train_timer += 1;
    $("#train-timer").text(train_timer.toString());
}

function initFrame() {
    var theH = $(window).height();
    $("#train-img").height(theH / 3);
    $(".num").height((theH - theH / 3 - 105) / 4);
    var dlgMargin = (theH / 3 + 50).toString() + "px";
    $("#modalDlg").css("margin-top", dlgMargin);
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

$('#myModal').on('hidden.bs.modal', function (e) {
    getPhoto();
    $("#train-input").text("");
    train_timer = 0;
    $("#train-timer").text("0");
    inputString = "";
});

$(document).bind('touchmove', function (event) {
    event.preventDefault();
});

//$(document).bind('touchend', function (event) {
//    //if (event.originalEvent.targetTouches[0].target.id != 'close_button') {
//        event.preventDefault();
//    //}
//});

$(document).bind('touchstart', function (event) {
    var tar = event.originalEvent.targetTouches[0].target;
    if (tar.id != 'close_button') {
        if (tar.id == 'train-timer' || tar.nodeName != 'BUTTON') {
            event.preventDefault();
        }
        else {
            var content = tar.innerText;
            if (content == "<-") {
                inputString = inputString.substring(0, inputString.length - 1);
                $("#train-input").text(inputString);
            }
            else if (content.length > 1) {
                inputString = $("#train-input").text();
                var myDate = new Date();
                var theContent = (myDate.getTime() - theTime).toString();
                if (inputString == theCode) {
                    theContent = "<h1>答案正确!</h1><br><strong>用时： " + theContent + " 毫秒</strong>";
                }
                else {
                    theContent = "<h1>答案错误！</h1><br><strong>正确答案为 ：" + theCode + "</strong>";
                }
                $("#modalContent").html(theContent);
                $('#myModal').modal();
            }
            else {
                inputString += content;
                $("#train-input").text(inputString);
            }
            event.preventDefault();
        }
    }
});

//document.body.addEventListener('touchmove', function (event) {
//    event.preventDefault();
//}, false);

//document.addEventListener('touchstart', function (event) {
//    var tar =event.touches[0].target;
//    if(tar.nodeName =='BUTTON')
//        tar.click();
//}, false);
//
//document.body.addEventListener('click', function (event) {
//    event.preventDefault();
//}, false);