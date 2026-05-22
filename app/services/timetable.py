from datetime import datetime, date, timezone, timedelta
from .csv_loader import get_data
from jpholiday import is_holiday
from requests import get
from bs4 import BeautifulSoup as bs


def get_ymd():
    return [int(x) for x in str(date.today()).split("-")]


def get_type(ymd=None):
    if ymd is None:
        ymd = get_ymd()
    x = date(ymd[0], ymd[1], ymd[2])
    if is_holiday(x):
        return "hd"
    weekday = x.weekday()
    if weekday <= 4:
        return "wd"
    if weekday == 5:
        return "st"
    return "hd"


def get_hhmm():
    hhmm = str(datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=9))))
    return [int(hhmm[11:13]), int(hhmm[14:16])]


def get_hour():
    return get_hhmm()[0]


def search(dest, type=None, hour=None, timetable=None):
    if type is None:
        type = get_type()
    if hour is None:
        hour = get_hour()
    if timetable is None:
        timetable = get_data("kyushukodaimae.csv")
    return [
        [int(xs[2]), int(xs[3])]
        for xs in timetable
        if (xs[0] == dest) and (xs[1] == type) and (hour <= int(xs[2]))
    ]


def minutize(hhmm):
    return hhmm[0] * 60 + hhmm[1]


def add_min(hhmm, m):
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
    response = get(url)
    response.encoding = response.apparent_encoding
    soup = bs(response.text, "html.parser")
    dt, dd = soup.find("dt"), soup.find("dd")
    if (dt and dd) and dd.p:
        return [True, dt.get_text(strip=True), dd.p.get_text(strip=True)]
    return [False]
