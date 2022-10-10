from application import app
from flask import render_template, request, json, Response, redirect, flash, url_for, session
from application.models import dimMedication
#from application.forms import LoginForm, RegisterForm
import psycopg2


@app.route("/")
def index():
    
    medications = dimMedication.query.all()
    return render_template("courses.html", index=True, courseData=medications)
