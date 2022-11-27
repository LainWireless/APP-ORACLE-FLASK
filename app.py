import os
import sys
import cx_Oracle
from flask import Flask, render_template, abort, request, redirect, url_for, abort

if sys.platform.startswith("darwin"):
    cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/instantclient_19_3")
elif sys.platform.startswith("win32"):
    cx_Oracle.init_oracle_client(lib_dir=r"c:\oracle\instantclient_19_8")

def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("""
        ALTER SESSION SET
          TIME_ZONE = 'UTC'
          NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI'""")


def start_pool():

    pool_min = 4
    pool_max = 4
    pool_inc = 0
    pool_gmd = cx_Oracle.SPOOL_ATTRVAL_WAIT

    print("Connecting to", os.environ.get("PYTHON_CONNECTSTRING"))

    pool = cx_Oracle.SessionPool(user='c##ivan',
                                 password='ivan',
                                 dsn=os.environ.get('192.168.122.177:1521/ORCLCDB'),
                                 min=pool_min,
                                 max=pool_max,
                                 increment=pool_inc,
                                 threaded=True,
                                 getmode=pool_gmd,
                                 sessionCallback=init_session)

    return pool

app = Flask(__name__)
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        text1=request.form.get("user")
        print ('text1=',text1)
        text2=request.form.get("pass")
        print ('text2=',text2)
        connection=cx_Oracle.connect(
            user=text1,
            password=text2,
            dsn='192.168.122.177:1521/ORCLCDB',
            encoding='UTF-8')
        if connection:
            cursor=connection.cursor()
            cursor.execute("select * from cat")
            resultado=cursor.fetchall()
            print(resultado)
            return render_template('datos.html',resultado=resultado)
        else:
            return render_template('login.html')
    else:
        return render_template("login.html")

if __name__ == '__main__':
    pool = start_pool()
    #app.run(port=int(os.environ.get('PORT', '8080')))
    app.run("0.0.0.0",5000,debug=True)
