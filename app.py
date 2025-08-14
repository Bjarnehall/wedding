import sqlite3
from flask import Flask, render_template, g
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
