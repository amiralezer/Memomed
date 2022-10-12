from application import app,db
from flask import  render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application.models import dimMedication, User, dimMedicationSchedule
from application.forms import LoginForm, RegisterForm
from flask_restx import Resource


@app.route('/esp32-medshedule')
def GetMedSchedule ():
    f=dimMedicationSchedule.query.all()
    return jsonify(f)

@app.route('/esp32-med')
def GetMed ():
    f=dimMedication.query.all()
    return jsonify(f)


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
   
    return render_template("index.html", index=True)


@app.route("/courses")
def courses():
    user_id = session['user_id']
    medications = dimMedicationSchedule.query.filter_by(user_id=user_id)
    print(medications)
    return render_template("courses.html", index=True, courseData=medications)

@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data

        user = User.query.filter_by(email=email).first() 
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/courses")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True )

@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('index'))


@app.route("/register", methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id     = User.query.count()
        user_id     += 1

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)