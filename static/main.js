// reference <https://takechi-web.com/javascript-current-time-display/#toc4>

function showtime() {
    var now = new Date();
    var text = now.getHours() + " 時 " + now.getMinutes() + " 分 " + now.getSeconds() + " 秒";
    document.getElementById("current-time").textContent = "現在時刻（JST）：" + text;
}

setInterval(() => {
    showtime()
}, 1000);
