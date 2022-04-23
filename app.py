from flask import Flask, render_template, jsonify
from jieba.analyse import extract_tags
import string
import sql_utils

app = Flask(__name__)


@app.route("/l1")
def get_l1_data():
    """
    data for div left 1
    """
    data = sql_utils.get_l1_data()
    day, confirm_add, heal_add = [], [], []
    for time, confirm, heal in data:
        day.append(time.strftime("%m-%d"))
        confirm_add.append(confirm)
        heal_add.append(heal)
    return jsonify({"day": day, "confirm_add": confirm_add, "heal_add": heal_add})


@app.route("/l2")
def get_l2_data():
    """
    data for div left 2
    """
    data = sql_utils.get_l2_data()
    details = []
    risk = []
    end_update_time = data[0][0]
    # a, b, c, d, e is address
    for a, b, c, d, e, type in data:
        risk.append(type)
        details.append(f"{b}\t{c}\t{d}\t{e}")
    return jsonify({"update_time": end_update_time, "details": details, "risk": risk})


@app.route("/c1")
def get_c1_data():
    """
    data for div center 1
    """
    data = sql_utils.get_c1_data()
    return jsonify({"confirm": int(data[0]), "confirm_now": int(data[1]), "heal": int(data[2]), "dead": int(data[3])})


@app.route("/c2")
def get_c2_data():
    """
    data for div center 2
    """
    res = []
    data = sql_utils.get_c2_data()
    for tup in data:
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


@app.route("/r1")
def get_r1_data():
    """
    data for div right 1
    """
    data = sql_utils.get_r1_data()
    city = []
    confirm = []
    for city_name, confirm_num in data:
        city.append(city_name)
        confirm.append(int(confirm_num))
    return jsonify({"city": city, "confirm": confirm})


@app.route("/r2")
def get_r2_data():
    """
    data for div right 2
    """
    data = sql_utils.get_r2_data()
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)  # Remove hot search numbers
        v = i[0][len(k):]  # Get hot search numbers
        ks = extract_tags(k)  # Using Jieba to extract keywords
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})
    return jsonify({"kws": d})


@app.route('/')
def hello_world():
    """
    render main.html
    """
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
