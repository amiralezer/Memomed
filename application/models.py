from dataclasses import dataclass
import flask
import flask_sqlalchemy
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.inspection import inspect
from flask import json
import datetime


@dataclass
class dimMedication (db.Model):
    MedicationID : int
    MedicationName : str
    __tablename__ = 'dimMedication'
    __table_args__ = {
        'schema': 'MEMOMED',
        'quote' : True
    }
    MedicationID = db.Column(db.Integer, primary_key=True)
    MedicationName = db.Column(db.String)

@dataclass
class dimMedicationSchedule (db.Model):

    MedicineID: int
    isDeleted: bool
    InitialMedicinePills : int
    InitialTime : datetime
    HoursApart : float
    user_id : int
    NextTime : datetime
    RemainingPills : int
    LastTime : datetime
    RecordID : int
    Drawer : int
    FlagESP : bool

    __tablename__ = 'dimMedicationSchedule'
    __table_args__ = {
        'schema': 'MEMOMED',
        'quote' : True
    }

    MedicineID = db.Column(db.Integer)
    isDeleted = db.Column(db.Boolean)
    InitialMedicinePills = db.Column(db.Integer)
    InitialTime = db.Column(db.DateTime)
    HoursApart = db.Column(db.Numeric)
    user_id =   db.Column(db.Integer)
    NextTime = db.Column(db.DateTime)
    RemainingPills = db.Column(db.Integer)
    LastTime = db.Column(db.DateTime)
    RecordID = db.Column(db.Integer, primary_key=True )
    Drawer =   db.Column(db.Integer)
    FlagESP = db.Column(db.Boolean)




@dataclass
class User(db.Model):
    user_id : int
    first_name : str
    last_name : str
    email : str
    password : str

    
    __tablename__ = 'dimUsers'
    __table_args__ = {
        'schema': 'MEMOMED',
        'quote' : True
    }
    user_id     =   db.Column(db.Integer, primary_key=True )
    first_name  =   db.Column(db.String)
    last_name   =   db.Column(db.String)
    email       =   db.Column(db.String, unique=True )
    password    =   db.Column(db.String)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)