import sqlite3
from flask import Flask, render_template, g, request
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route("/information")
def info():
    return render_template(
        "info.html"
    )

@app.route("/location")
def location():
    return render_template(
        "location.html"
    )

@app.route("/sign_up")
def sign_up():
    return render_template(
        "sign_up.html"
    )

@app.route("/sign_up_server", methods=["POST"])
def sign_up_server():

    name = request.form.get("fullname")
    name_partner = request.form.get("partner_name")
    email = request.form.get("email")
    phone_number = request.form.get("phone")
    special_request = request.form.get("special_field")
    sleep_over = request.form.get("sleep_over_field")

    if special_request == "":
        special_request = "Nej"

    if sleep_over == "":
        sleep_over = "Nej"
    
    if name == "" or (email == "" and phone_number == ""):
        return render_template("sign_up.html", show_alert="true")

    if name_partner:
        name = f"{name} & {name_partner}"

    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO guests (name, email, phone_number, special_request, sleep_over)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (name, email, phone_number, special_request, sleep_over)
    )
    conn.commit()
    cur.close()
    conn.close()

    return render_template(
        "sign_up_valid.html",
        name=name,
        email=email,
        phone_number=phone_number,
        special_request=special_request,
        sleep_over=sleep_over
    )

@app.route("/guest_list")
def guest_list():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM guests")
    guests = cur.fetchall()
    cur.close()
    conn.close()

    return render_template(
        "guest_list.html",
        guests=guests
    )


if __name__ == "__main__":
    app.run(debug=True)
