// reference <https://takechi-web.com/javascript-current-time-display/#toc4>

function showtime() {
    const now = new Date();
    document.getElementById("digital-clock").textContent = "現在時刻（JST）：" +
        now.getHours() + " 時 " + now.getMinutes() + " 分 " + now.getSeconds() + " 秒";
}

setInterval(() => {
    showtime()
}, 1000);
