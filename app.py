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
        texto=request.form.get("user")
        print ('texto=',texto)
        texto2=request.form.get("pass")
        print ('texto2=',texto2)
        if texto=='c##ivan' and texto2=='ivan':
            connection=cx_Oracle.connect(
	        user='c##ivan',
	        password='ivan',
	        dsn='192.168.122.177:1521/ORCLCDB',
	        encoding='UTF-8')
            cursor = connection.cursor()
            cursor.execute("select codigo from agentes")
            resultado = cursor.fetchall()
            cursor.execute("select sucursal from agentes")
            resultado2 = cursor.fetchall()
            cursor.execute("select nombre from agentes")
            resultado3 = cursor.fetchall()
            cursor.execute("select area_trabajo from agentes")
            resultado4 = cursor.fetchall()
            cursor.execute("select comision from agentes")
            resultado5 = cursor.fetchall()
            cursor.execute("select telefono from agentes")
            resultado6 = cursor.fetchall()
            cursor.execute("select pais from agentes")
            resultado7 = cursor.fetchall()
            return render_template("datos.html",resultado=resultado,resultado2=resultado2,resultado3=resultado3,resultado4=resultado4,resultado5=resultado5,resultado6=resultado6,resultado7=resultado7)
        else:
            return redirect(url_for('login'))
    else:
        return render_template("login.html")

if __name__ == '__main__':
    pool = start_pool()
    #app.run(port=int(os.environ.get('PORT', '8080')))
    app.run("0.0.0.0",5000,debug=True)