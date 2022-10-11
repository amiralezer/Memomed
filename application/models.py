import flask
import flask_sqlalchemy
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON


class dimMedication (db.Model):
    __tablename__ = 'dimMedication'
    __table_args__ = {
        'schema': 'MEMOMED',
        'quote' : True
    }
    MedicineID = db.Column(db.Integer, primary_key=True)
    MedicineName = db.Column(db.String)
    MedicinePills = db.Column(db.Integer)
    InitialTime = db.Column(db.DateTime)
    HoursApart = db.Column(db.Numeric)


class User(db.Model):
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

# class Course(db.Document):
#     courseID   =   db.StringField( max_length=10, unique=True )
#     title       =   db.StringField( max_length=100 )
#     description =   db.StringField( max_length=255 )
#     credits     =   db.IntField()
#     term        =   db.StringField( max_length=25 )

# class Enrollment(db.Document):
#     user_id     =   db.IntField()
#     courseID    =   db.StringField( max_length=10 )