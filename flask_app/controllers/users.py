from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template("index.html")
