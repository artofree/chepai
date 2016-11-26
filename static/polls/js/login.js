$(document).ready(function () {
    var b = detect.parse(navigator.userAgent);
    if(b.browser.family !='Chrome'){
        $('#maincontent').html('<h1>浏览器不兼容，请使用谷歌chrome浏览器，可自行下载安装或到群文件里下载</h1>');
    }
});