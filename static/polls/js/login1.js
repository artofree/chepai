$(document).ready(function () {
    var b = detect.parse(navigator.userAgent);
    if(b.browser.family !='Chrome' &&b.browser.family !='Firefox'){
        $('#maincontent').html('<h1>浏览器不兼容，请使用谷歌chrome浏览器或firefox浏览器，可自行下载安装或到群文件里下载</h1>');
    }
});