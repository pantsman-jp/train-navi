from csv import writer, reader
from datetime import datetime, date
from jpholiday import is_holiday
from requests import get
from bs4 import BeautifulSoup as bs


def make_timetable(fname):
    """
    destination, daytime, hour, minute
    destination = (hakata, kokura)
    daytime = (weekday, saturday, holiday)
    hour = 0 ~ 23
    minute = 0 ~ 59
    """
    with open(fname, mode="a", newline="") as f:
        print("終了は 'end' で")
        print("形式：[hakata/kokura] [wd/st/hd] [hour] [min]")
        while True:
            data = list(input("destination daytime hour minute >>> ").split())
            if data[0] == "end":
                break
            if len(data) != 4:
                print("【形式エラー】再入力してください。")
                return make_timetable(fname)
            try:
                writer(f).writerow(data)
            except Exception:
                print("【エラー】再入力してください。")
                return make_timetable(fname)
    print(str(fname) + " に保存しました。")


def get_data(fname):
    return [xs for xs in reader(open(fname, mode="r"))]


def search(dest, type, hour, xss=get_data("kyushukodaimae.csv")):
    return [
        [int(xs[2]), int(xs[3])]
        for xs in xss
        if (xs[0] == dest) and (xs[1] == type) and (hour <= int(xs[2]))
    ]


def get_hhmm():
    hhmm = str(datetime.now())
    return [int(hhmm[11:13]), int(hhmm[14:16])]


def get_hour():
    return get_hhmm()[0]


def get_ymd():
    return [int(x) for x in str(date.today()).split("-")]


def get_type(ymd=get_ymd()):
    x = date(ymd[0], ymd[1], ymd[2])
    if is_holiday(x):
        return "hd"
    type = x.weekday()
    if type <= 4:
        return "wd"
    if type == 5:
        return "st"
    return "hd"


def minutize(hhmm):
    return hhmm[0] * 60 + hhmm[1]


def is_in_time(place, dest):
    now = minutize(get_hhmm())
    walk_time = {1: 8, 2: 11, 3: 12, 4: 16, 5: 18}[int(place)]
    run_time = walk_time // 1.4
    tt = search(dest, get_type(), get_hhmm()[0])
    for row in tt:
        departure = minutize(row)
        if now + walk_time <= departure:
            row.append("walk")
        elif now + run_time <= departure:
            row.append("run")
        else:
            row.append("fail")
    return tt


def get_service_status(url="https://transit.yahoo.co.jp/diainfo/386/386"):
    """[reference](https://qiita.com/hirohiroto522/items/6ff29be1344be805ecb0)"""
    response = get(url)
    response.encoding = response.apparent_encoding
    soup = bs(response.text, "html.parser")
    dt, dd = soup.find("dt"), soup.find("dd")
    if (dt and dd) and dd.p:
        return [True, dt.get_text(strip=True), dd.p.get_text(strip=True)]
    return [False]


# make_timetable("timetable.csv")
# print(get_hhmm())
# print(get_type())
# print(search("kokura", get_type(), get_hour()))
# print(is_in_time(1, "kokura"))
