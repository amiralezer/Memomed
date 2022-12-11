from sqlalchemy import null, func
from application import app,db,scheduler
from flask import  render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application.models import dimMedication, User, dimMedicationSchedule
from application.forms import LoginForm, RegisterForm, AddMedicationForm
from flask_restx import Resource
from datetime import datetime,timedelta


@scheduler.task('interval', id='do_job_2', seconds=30)
def job2():
    print('job triggado')
    timeneededplus = datetime.now() + timedelta(seconds=30)
    aux = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.RecordID).filter(dimMedicationSchedule.NextTime <=timeneededplus\
                                                     ,dimMedicationSchedule.FlagESP == False\
    #                                                 ,dimMedicationSchedule.NextTime >=timeneededminus\
                                                     ,dimMedicationSchedule.isDeleted == False).all()

    if len(aux) != 0 :
        print("entrei no if")
        print(aux)
        for row in aux:
            UpdateSchedulee(row.RecordID)
    return ('Job finished')

def UpdateSchedulee(recordid):   
    print('update schedule triggado')

    print(recordid)
    NextTime = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.NextTime)\
                                                        .filter(dimMedicationSchedule.RecordID == recordid).first()
    LastTimeUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                            .update({'LastTime':NextTime})                                                
    HoursApart = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.HoursApart)\
                                                        .filter(dimMedicationSchedule.RecordID == recordid).first()
    hoursfinal =str(HoursApart[0])
    h= hoursfinal.split('.')[0]
    m = hoursfinal.split('.')[1]
    NextTimeDate = NextTime[0] + timedelta(hours=int(h)) + timedelta(minutes=(int(m)*60/20)) # dividindo por 20 p deixar test friendly

    
    if (dimMedicationSchedule.query.with_entities(dimMedicationSchedule.RemainingPills)\
                                                        .filter(dimMedicationSchedule.RecordID == recordid).first()[0] - 1 == 0):
        Pills = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                             .update({'RemainingPills':dimMedicationSchedule.RemainingPills -1,'isDeleted':True })                                                
    else:
        Pills = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                             .update({'RemainingPills':dimMedicationSchedule.RemainingPills -1})  
    
    NextTimeUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                             .update({'NextTime':NextTimeDate})     
    EspUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                            .update({'FlagESP':False})
    db.session.commit()


# @scheduler.task('interval', id='do_job_1', seconds=30)
# def job1():
#     fmt = '%d/%m/%Y %H:%M'
#     def UpdateSchedulee(recordid):
#         print('job triggado')
#         print(recordid)
#         NextTime = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.NextTime)\
#                                                         .filter(dimMedicationSchedule.RecordID == recordid).first()
#         LastTimeUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
#                                             .update({'LastTime':NextTime})                                                
#         HoursApart = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.HoursApart)\
#                                                         .filter(dimMedicationSchedule.RecordID == recordid).first()
#         hoursfinal =str(HoursApart[0])
#         h= hoursfinal.split('.')[0]
#         m = hoursfinal.split('.')[1]
#         NextTimeDate = NextTime[0] + timedelta(hours=int(h)) + timedelta(minutes=(int(m)*60/10))

    
#         if (dimMedicationSchedule.query.with_entities(dimMedicationSchedule.RemainingPills)\
#                                                         .filter(dimMedicationSchedule.RecordID == recordid).first()[0] - 1 == 0):
#             Pills = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
#                                              .update({'RemainingPills':dimMedicationSchedule.RemainingPills -1,'isDeleted':True })                                                
#         else:
#             Pills = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
#                                              .update({'RemainingPills':dimMedicationSchedule.RemainingPills -1})  
    
#         NextTimeUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
#                                              .update({'NextTime':NextTimeDate})     
#         EspUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
#                                             .update({'FlagESP':False})
#         db.session.commit()
#     timeneededplus = datetime.now() + timedelta(seconds=30)
#     #timeneededminus = datetime.now() + timedelta(seconds=-30)

#     aux = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.RecordID).filter(dimMedicationSchedule.NextTime <=timeneededplus\
#                                                      ,dimMedicationSchedule.FlagESP == False\
#     #                                                 ,dimMedicationSchedule.NextTime >=timeneededminus\
#                                                      ,dimMedicationSchedule.isDeleted == False).all()
#     if len(aux) != 0 :
#         print("entrei no if")
#         print(aux)
#         for row in aux:
#             UpdateSchedulee(row.RecordID)


    


   
@app.route('/post/<recordid>',methods=['GET','POST'])
def UpdateSchedule(recordid):
    EspData = request.data

    NextTime = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.NextTime)\
                                                        .filter(dimMedicationSchedule.RecordID == recordid).first()
    LastTimeUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                            .update({'LastTime':NextTime})                                                
    HoursApart = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.HoursApart)\
                                                        .filter(dimMedicationSchedule.RecordID == recordid).first()
    hoursfinal =str(HoursApart[0])
    h= hoursfinal.split('.')[0]
    m = hoursfinal.split('.')[1]
    NextTimeDate = NextTime[0] + timedelta(hours=int(h)) + timedelta(minutes=(int(m)*60/10))

    
    if (dimMedicationSchedule.query.with_entities(dimMedicationSchedule.RemainingPills)\
                                                        .filter(dimMedicationSchedule.RecordID == recordid).first()[0] - 1 == 0):
        Pills = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                             .update({'RemainingPills':dimMedicationSchedule.RemainingPills -1,'isDeleted':True })                                                
    else:
        Pills = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                             .update({'RemainingPills':dimMedicationSchedule.RemainingPills -1})  
    
    NextTimeUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                             .update({'NextTime':NextTimeDate})     
    EspUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                            .update({'FlagESP':False})
    db.session.commit()
    return redirect(url_for('schedule'))






@app.route('/get-user/<email>')
def GetUser (email):
    getUserid = User.query.with_entities(User.user_id).filter_by(email=email).first()
    return jsonify(getUserid)

@app.route('/esp32-medshedule/<user_id>')
def GetMedSchedule (user_id):
    user_id = user_id
    medSchedule=dimMedicationSchedule.query.filter_by(user_id=user_id,isDeleted=False).all()
    return jsonify(medSchedule)

@app.route('/esp32-med')
def GetMed ():
    med=dimMedication.query.all()
    return jsonify(med)


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    print(dimMedicationSchedule.query.filter_by(Drawer=1).first())
    return render_template("index.html", index=True)


@app.route("/schedule")
def schedule():
    user_id = session['user_id']
    medications = dimMedicationSchedule.query.join(dimMedication, dimMedicationSchedule.MedicineID==dimMedication.MedicationID)\
        .add_columns(dimMedication.MedicationName,dimMedicationSchedule.RecordID, dimMedicationSchedule.InitialTime,dimMedicationSchedule.NextTime,dimMedicationSchedule.LastTime, dimMedicationSchedule.InitialMedicinePills,dimMedicationSchedule.RemainingPills,dimMedicationSchedule.HoursApart,dimMedicationSchedule.Drawer)\
        .filter(dimMedicationSchedule.user_id == user_id)\
        .filter(dimMedicationSchedule.isDeleted == False)\
        .order_by(dimMedicationSchedule.Drawer).all()
    
    return render_template("schedule.html", schedule=True, courseData=medications,lenCourseData = len(medications))

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
            return redirect("/schedule")
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

@app.route("/addbutton",methods=['POST','GET'])
def addbutton():
    names = dimMedication.query.with_entities(dimMedication.MedicationName).all()
    form = AddMedicationForm()
    form.MedName.choices = [ g.MedicationName for g in names]

    if form.validate_on_submit():
        RecordIDs= dimMedicationSchedule.query.with_entities(dimMedicationSchedule.RecordID).all()
        values = [ RecordIDd[0] for RecordIDd in RecordIDs ]
        if values:
            RecordID = max(values) + 1
        else :
            RecordID=1
        MedicineID = dimMedication.query.with_entities(dimMedication.MedicationID).filter_by(MedicationName=form.MedName.data).first()
        isDeleted = False
        InitialMedicinePills = form.InitialPills.data
        InitialTime = (datetime.strptime(form.InitialTime.data,'%d/%m/%Y %H:%M'))
        HoursApart = form.HoursDiff.data
        userId = session['user_id']
        h = HoursApart.split('.')[0]
        m = HoursApart.split('.')[1]
        Drawer = form.Drawer.data
        NextTime = (datetime.strptime(form.InitialTime.data,'%d/%m/%Y %H:%M') + timedelta(hours=int(h)) + timedelta(minutes=(int(m)*60/10)))
        RemainingPills = form.InitialPills.data
        LastTime = None
        FlagESP = False
        MedRecord = dimMedicationSchedule(MedicineID=MedicineID,isDeleted=isDeleted,InitialMedicinePills=InitialMedicinePills,InitialTime=InitialTime,HoursApart=HoursApart,user_id=userId,NextTime=NextTime,RemainingPills=RemainingPills,LastTime=LastTime,Drawer=Drawer,RecordID=RecordID,FlagESP=FlagESP)
        print(MedRecord)
        db.session.add(MedRecord)
        db.session.commit()
        flash("Medicação Adicionada com sucesso","success")
        return redirect(url_for('schedule'))
    return render_template("addmedication.html", title="Adicionar Medicamento", form=form)
   
@app.route("/delete/<medid>",methods=['POST','GET'])
def delmed(medid):
    med = dimMedicationSchedule.query.filter_by(RecordID=medid).update({'isDeleted':True})
    db.session.commit()
    flash("Medicação Removida com sucesso","success")
    return redirect(url_for('schedule'))


def UpdateScheduleteste(recordid):
  

    NextTime = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.NextTime)\
                                                        .filter(dimMedicationSchedule.RecordID == recordid).first()
    LastTimeUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                            .update({'LastTime':NextTime})                                                
    HoursApart = dimMedicationSchedule.query.with_entities(dimMedicationSchedule.HoursApart)\
                                                        .filter(dimMedicationSchedule.RecordID == recordid).first()
    hoursfinal =str(HoursApart[0])
    h= hoursfinal.split('.')[0]
    m = hoursfinal.split('.')[1]
    NextTimeDate = NextTime[0] + timedelta(hours=int(h)) + timedelta(minutes=(int(m)*60/10))

    
    if (dimMedicationSchedule.query.with_entities(dimMedicationSchedule.RemainingPills)\
                                                        .filter(dimMedicationSchedule.RecordID == recordid).first()[0] - 1 == 0):
        Pills = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                             .update({'RemainingPills':dimMedicationSchedule.RemainingPills -1,'isDeleted':True })                                                
    else:
        Pills = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                             .update({'RemainingPills':dimMedicationSchedule.RemainingPills -1})  
    
    NextTimeUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                             .update({'NextTime':NextTimeDate})     
    EspUpdate = dimMedicationSchedule.query.filter(dimMedicationSchedule.RecordID == recordid)\
                                            .update({'FlagESP':False})
    db.session.commit()
    return redirect(url_for('schedule'))

