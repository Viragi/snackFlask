from flask import Flask, request, url_for, render_template, redirect
from flask_modus import Modus
from flask_debugtoolbar import DebugToolbarExtension
import psycopg2


def connect():
    c = psycopg2.connect("dbname=flask-sql")
    return c


app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
modus = Modus(app)
toolbar = DebugToolbarExtension(app)


class Snack:
    count = 1

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.id = Snack.count
        Snack.count += 1

    def getName(self):
        return self.name


# waffles = Snack("waffles one", 12)
# mangoes = Snack("mangoes", 10)
# snacks = [waffles, mangoes]


@app.route("/snack", methods=["GET"])
def get_snack_list():
    with psycopg2.connect("postgresql://localhost/snacks") as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, price FROM snack_details")
        snacks = c.fetchall()
        snacks = [{"id": t[0], "name": t[1], "price": t[2]} for t in snacks]
    return render_template("snacklist.html", snacks=snacks)


# return render_template("snacklist.html", snacks=snacks)


@app.route("/snack/add", methods=["get"])
def new_snack_form():
    return render_template("addsnack.html")


@app.route("/snack", methods=["POST"])
def add_snack():
    new_snack = Snack(request.form['name'], request.form['price'])
    with psycopg2.connect("postgresql://localhost/snacks") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO snacks(name,price) VALUES(%s,%s)",
                  (name, price))
    return redirect({{url_for(get_snack_list)}})
    # snacks.append(new_snack)
    # return redirect("/snack")


@app.route("/snack/edit/<int:snackid>", methods=["GET"])
def edit_snack(snackid):
    # name1 = request.args.get["name"]
    # price1 = request.args.get["price"]
    # print(name1, price1)
    s = [s for s in snacks if s.id == snackid][0]
    name1 = s.name
    val = s.price

    return render_template("edit.html", name=name1, price=val, id=snackid)


@app.route("/snack/<int:id>", methods=["PATCH"])
def update_snack(id):
    s = [s for s in snacks if s.id == id][0]
    s.name = request.form["name"]
    s.price = request.form["price"]
    return redirect("/snack")


@app.route("/snack/<int:id>", methods=["DELETE"])
def delete_snack(id):
    s = [s for s in snacks if s.id == id][0]
    snacks.remove(s)
    return redirect("/snack")
