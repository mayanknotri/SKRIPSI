from flask import render_template, request
from app import app
import pandas as pd


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
