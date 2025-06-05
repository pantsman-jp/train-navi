from flask import Flask, render_template, request, redirect, url_for
from functions import (
    is_in_time,
    get_service_status,
    merge,
    search,
    calc_arrtime,
    get_time_ex,
    get_time_shin,
    attach_all_arrival_times,
)

app = Flask("TrainNavi")
ver = "v0.9.0"
debug = True


@app.route("/", methods=["GET", "POST"])
def index():
    print("index")
    if request.method == "POST":
        place, dest = request.form.get("place"), request.form.get("destination")
        if dest == "kokura":
            return redirect(url_for("kokura", place=place))
        else:
            return redirect(url_for("hakata", place=place))
    return render_template("index.jinja", ver=ver, status=get_service_status())


@app.route("/forkokura", methods=["GET"])
def kokura():
    print("kokura")
    place, dest = request.args.get("place"), "kokura"
    return render_template(
        "forkokura.jinja",
        ver=ver,
        timetable=merge(is_in_time(place, dest), calc_arrtime(search(dest), 5)),
    )


@app.route("/forhakata", methods=["GET"])
def hakata():
    place, dest = request.args.get("place"), "hakata"
    return render_template(
        "forhakata.jinja",
        ver=ver,
        timetable=attach_all_arrival_times(
            is_in_time(place, dest), get_time_ex(dest), get_time_shin(dest)
        ),
    )


def start_server(debug):
    app.run(host="localhost", port=5000, debug=debug)


def start_server2(debug):
    app.run(host="0.0.0.0", port=5050, debug=debug)


# start_server(debug)
start_server2(debug)
