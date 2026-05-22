// reference <https://takechi-web.com/javascript-current-time-display/#toc4>

function getJstDate() {
    const now = new Date();
    const utc = now.getTime() + now.getTimezoneOffset() * 60000;
    return new Date(utc + 9 * 60 * 60000);
}

function showtime() {
    const now = getJstDate();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();

    document.getElementById("digital-clock").textContent =
        `現在時刻（JST）：${hours} 時 ${minutes} 分 ${seconds} 秒`;

    const hourDegrees = (hours % 12) * 30 + minutes * 0.5;
    const minuteDegrees = minutes * 6 + seconds * 0.1;
    const secondDegrees = seconds * 6;

    document.getElementById("hour-hand").style.transform =
        `translate(-50%, -100%) rotate(${hourDegrees}deg)`;
    document.getElementById("minute-hand").style.transform =
        `translate(-50%, -100%) rotate(${minuteDegrees}deg)`;
    document.getElementById("second-hand").style.transform =
        `translate(-50%, -100%) rotate(${secondDegrees}deg)`;
}

showtime();
setInterval(showtime, 1000);
