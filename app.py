from flask import Flask, render_template, request, redirect, url_for
from functions import is_in_time, get_service_status

app = Flask("TrainNavi")
ver = "v0.7.0"
debug = True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place, dest = request.form.get("place"), request.form.get("destination")
        return redirect(url_for("result", place=place, destination=dest))
    return render_template("index.jinja", ver=ver, status=get_service_status())


@app.route("/result", methods=["GET"])
def result():
    place, dest = request.args.get("place"), request.args.get("destination")
    return render_template(
        "result.jinja",
        dst=dest,
        ver=ver,
        timetable=is_in_time(place, dest),
    )


def start_server(debug):
    app.run(host="localhost", port=5000, debug=debug)


def start_server2(debug):
    app.run(host="0.0.0.0", port=5000, debug=debug)


start_server(debug)
# start_server2(debug)
