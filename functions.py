from csv import writer, reader
from datetime import datetime, date, timezone, timedelta
from jpholiday import is_holiday
from requests import get
from bs4 import BeautifulSoup as bs


def get_data(fname):
    """
    get timetable data from fname.csv
    by pantsman
    """
    return [xs for xs in reader(open(fname, mode="r"))]


def get_ymd():
    """
    get data [yyyy,mm,dd]
    by pantsman
    """
    return [int(x) for x in str(date.today()).split("-")]


def get_type(ymd=get_ymd()):
    """
    get today's date type
    by pantsman
    """
    x = date(ymd[0], ymd[1], ymd[2])
    if is_holiday(x):
        return "hd"
    type = x.weekday()
    if type <= 4:
        return "wd"
    if type == 5:
        return "st"
    return "hd"


def get_hhmm():
    """
    get current time
    by pantsman
    """
    hhmm = str(datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=9))))
    return [int(hhmm[11:13]), int(hhmm[14:16])]


def get_hour():
    """
    get current hour
    by pantsman
    """
    return get_hhmm()[0]


def search(
    dest, type=get_type(), hour=get_hour(), timetable=get_data("kyushukodaimae.csv")
):
    """
    Search the timetable for train information
    that matches the destination, time, and day of the week.
    get all timetables after the search time
    by pantsman
    """
    return [
        [int(xs[2]), int(xs[3])]
        for xs in timetable
        if (xs[0] == dest) and (xs[1] == type) and (hour <= int(xs[2]))
    ]


def minutize(hhmm):
    return hhmm[0] * 60 + hhmm[1]


def add_min(hhmm, m):
    """
    >>> add_min([12,34],20)
    [12, 54]
    >>> add_min([13,55],7)
    [14, 2]
    >>> add_min([24,00],66)
    [25, 6]
    """
    total_minutes = hhmm[0] * 60 + hhmm[1] + m
    return [total_minutes // 60, total_minutes % 60]


def calc_arrtime(timetable, m):
    return [add_min(xs[:2], m) for xs in timetable]


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


def get_time_ex(dest="hakata"):
    times = []
    for local_time in search(dest):
        local_dep = minutize(local_time)
        transfer_arrival = local_dep + 2
        for express_time in search(dest, timetable=get_data("tobata_express.csv")):
            express_dep = minutize(express_time)
            if express_dep >= transfer_arrival:
                times.append(express_dep + 43 - local_dep)
                break
    return times


def get_time_shin(dest="hakata"):
    times = []
    for local_time in search(dest):
        local_dep = minutize(local_time)
        transfer_arrival = local_dep + 5
        for express_time in search(dest, timetable=get_data("kokura_shinkansen.csv")):
            express_dep = minutize(express_time)
            if express_dep >= transfer_arrival:
                times.append(express_dep + 15 - local_dep)
                break
    return times


def attach_all_arrival_times(timetable, durations_ex, durations_shin):
    length = min(len(timetable), len(durations_ex), len(durations_shin))
    result = []
    for i in range(length):
        hh, mm, fail = timetable[i]
        hh1, mm1 = add_min([hh, mm], durations_ex[i])
        hh2, mm2 = add_min([hh, mm], durations_shin[i])
        result.append([hh, mm, fail, hh1, mm1, hh2, mm2])
    return result


def merge(xss, yss):
    return [list(xy[0] + xy[1]) for xy in zip(xss, yss)]


def get_service_status(url="https://transit.yahoo.co.jp/diainfo/386/386"):
    """[reference](https://qiita.com/hirohiroto522/items/6ff29be1344be805ecb0)"""
    response = get(url)
    response.encoding = response.apparent_encoding
    soup = bs(response.text, "html.parser")
    dt, dd = soup.find("dt"), soup.find("dd")
    if (dt and dd) and dd.p:
        return [True, dt.get_text(strip=True), dd.p.get_text(strip=True)]
    return [False]


# def make_timetable(fname):
#     """
#     destination, daytime, hour, minute
#     destination = (hakata, kokura)
#     daytime = (weekday, saturday, holiday)
#     hour = 0 ~ 23
#     minute = 0 ~ 59
#     """
#     with open(fname, mode="a", newline="") as f:
#         print("終了は 'end' で")
#         print("形式：[hakata/kokura] [wd/st/hd] [hour] [min]")
#         while True:
#             data = list(input("destination daytime hour minute >>> ").split())
#             if data[0] == "end":
#                 break
#             if len(data) != 4:
#                 print("【形式エラー】再入力してください。")
#                 return make_timetable(fname)
#             try:
#                 writer(f).writerow(data)
#             except Exception:
#                 print("【エラー】再入力してください。")
#                 return make_timetable(fname)
#     print(str(fname) + " に保存しました。")
