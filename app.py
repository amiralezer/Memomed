from flask import Flask, render_template
import csv 
import psycopg2

host = 'mydb.cpvcbkzvvjux.us-east-1.rds.amazonaws.com'
database = 'memomed'
user = 'memomed'
password = 'memomedmemomed'
app = Flask(__name__)

@app.route('/')
def index():
    conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password)
    a = doQuery( conn )
    conn.close()
    medicineid = [a[0][0],a[1][0],a[2][0],a[3][0]]
    medicinenames = [a[0][1],a[1][1],a[2][1],a[3][1]]
    pillsqnt = [a[0][3],a[1][3],a[2][3],a[3][3]]
    initialtime = [str(a[0][4]),str(a[1][4]),str(a[2][4]),str(a[3][4])]
    hoursdiff = [float(a[0][5]),float(a[1][5]),float(a[2][5]),float(a[3][5])]
    return render_template('index.html',medicineid = medicineid,medicinenames=medicinenames,pillsqnt=pillsqnt,initialtime=initialtime,hoursdiff=hoursdiff)

def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute("SELECT * FROM \"MEMOMED\".\"dimMedication\"")
    return cur.fetchall()
    

if __name__ == '__main__':
   app.run(debug=True)