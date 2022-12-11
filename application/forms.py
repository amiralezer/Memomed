from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import email_validator
from application.models import User,dimMedicationSchedule
import numpy as np
import datetime
from datetime import timedelta
from flask import session,flash
import math

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
            raise ValidationError("Email ja cadastrado. Realize o login.")

class AddMedicationForm(FlaskForm):
    PillsNum = list(range(1, 13))
    HourNum = np.arange(0.1,24.5,0.1)
    #original#TimeNum = [x.strftime('%d/%m/%Y %H:%M') for x in [(datetime.datetime.min + math.ceil((datetime.datetime.now() - datetime.datetime.min) / timedelta(minutes=3)) * timedelta(minutes=3)) + datetime.timedelta(minutes=3*x) for x in range(1, 145)]]
    #teste
    TimeNum = [x.strftime('%d/%m/%Y %H:%M') for x in [(datetime.datetime.min + math.floor((datetime.datetime.now() - datetime.datetime.min) / timedelta(minutes=2)) * timedelta(minutes=2)) + datetime.timedelta(minutes=2*x) for x in range(1, 145)]]
    
    DrawNum = list(range(1, 5))
    MedName   = SelectField("Nome Remedio", validators=[DataRequired()])
    InitialPills = SelectField("Numero de comprimidos", validators=[DataRequired()],choices=PillsNum)
    InitialTime = SelectField("Inicio Medicação:", validators=[DataRequired()],choices=TimeNum)
    Drawer = SelectField("Gaveta:", validators=[DataRequired()],choices=DrawNum)
    HoursDiff = SelectField("Tempo entre doses (horas)", validators=[DataRequired()],choices = HourNum)
    submit = SubmitField("Cadastrar Medicamento")

    def validate_Drawer (self,Drawer):
        drawer = dimMedicationSchedule.query.filter_by(Drawer=Drawer.data,user_id=session["user_id"],isDeleted=False).first()
        if drawer:
            raise ValidationError("Gaveta em uso. Escolha outra!")

    def validate_InitialTime (self,InitialTime):
        
         iniTime = dimMedicationSchedule.query.filter_by(InitialTime=datetime.datetime.strptime(InitialTime.data, '%d/%m/%Y %H:%M'),user_id=session["user_id"],isDeleted=False).first()
         if iniTime:
            raise ValidationError("Horario inicial de outro medicamento. Escolha outro!")



