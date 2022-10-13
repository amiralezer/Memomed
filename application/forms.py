from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import email_validator
from application.models import User
import numpy as np
import datetime

class LoginForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(),Length(min=2,max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(),Length(min=2,max=55)])
    submit = SubmitField("Register Now")

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError("Email is already in use. Pick another one.")

class AddMedicationForm(FlaskForm):
    PillsNum = list(range(1, 13))
    HourNum = np.arange(0.05,24.5,0.05)
    TimeNum = [x.strftime('%d/%m/%Y %H:%M') for x in [datetime.datetime.now() + datetime.timedelta(minutes=2*x) for x in range(1, 145)]]
    DrawNum = list(range(1, 6))
    MedName   = SelectField("Nome Remedio", validators=[DataRequired()])
    InitialPills = SelectField("Numero de comprimidos", validators=[DataRequired()],choices=PillsNum)
    InitialTime = SelectField("Inicio Medicação:", validators=[DataRequired()],choices=TimeNum)
    Drawer = SelectField("Gaveta:", validators=[DataRequired()],choices=DrawNum)
    HoursDiff = SelectField("Tempo entre doses (horas)", validators=[DataRequired()],choices = HourNum)
    submit = SubmitField("Cadastrar Medicamento")



