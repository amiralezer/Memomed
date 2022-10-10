from application import app
from flask import render_template, request, json, Response, redirect, flash, url_for, session
#from application.models import User, Course, Enrollment
#from application.forms import LoginForm, RegisterForm


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True )