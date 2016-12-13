$(document).ready(function () {
    var myDate = new Date();
    theTime = myDate.getTime();
    $.get(parms.getusrname, function (ret) {
        var sDate = new Date();
        var sTime =sDate.getTime() -theTime;
        $.get(parms.getrsptime,
            {
                times: sTime
            },
            function (data, status) {
            });
    });
});