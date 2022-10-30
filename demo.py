"""
demo.py

Antes de ejecutar el programa establece unas variables de entorno:

    PYTHON_USERNAME       - El ususario de la base de datos
    PYTHON_PASSWORD       - La contraseña del usuario
    PYTHON_CONNECTSTRING  - El nombre o dirección del host donde se encuentra y el nombre de la sesión. "example.com/XEPDB1"
    PORT                  - El puerto por el que se va a servir la app web, por defecto es el 8080 

"""
# Importamos las funciones del sistema, el módulo que conecta python con oracle y flask para la aplicación en cuestión.
import os
import sys
import cx_Oracle
from flask import Flask, render_template, abort,request
from flask import Flask

################################################################################
# Esta parte del código es por si se inicia en otro sistema operativo.

if sys.platform.startswith("darwin"):
    cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/instantclient_19_3")
elif sys.platform.startswith("win32"):
    cx_Oracle.init_oracle_client(lib_dir=r"c:\oracle\instantclient_19_8")


# Init_session es una función para una llamada de sesión eficiente.

def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("""
        ALTER SESSION SET
          TIME_ZONE = 'UTC'
          NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI'""")

# Función para establecer la conexión con la base de datos
def start_pool():

    # Creamos las conexión con la base de datos usando variables de entorno.
    # Las variables de entorno en este caso son 
        #[oracle@bd ~]$ export PYTHON_CONNECTSTRING=localhost/ORCLCDB
        #[oracle@bd ~]$ export PYTHON_PASSWORD=ivan
        #[oracle@bd ~]$ export PYTHON_USERNAME=c##ivan
    
    pool_min = 4
    pool_max = 4
    pool_inc = 0
    pool_gmd = cx_Oracle.SPOOL_ATTRVAL_WAIT

    print("Connecting to", os.environ.get("PYTHON_CONNECTSTRING"))

    pool = cx_Oracle.SessionPool(user=os.environ.get("PYTHON_USERNAME"),
                                 password=os.environ.get("PYTHON_PASSWORD"),
                                 dsn=os.environ.get("PYTHON_CONNECTSTRING"),
                                 min=pool_min,
                                 max=pool_max,
                                 increment=pool_inc,
                                 threaded=True,
                                 getmode=pool_gmd,
                                 sessionCallback=init_session)

    return pool

################################################################################

# Definimos el nombre de la aplicación para flask
app = Flask(__name__)

# Muestra la página principal con su correspondiente plantilla
@app.route('/',methods=["GET","POST"])
def inicio():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("select * from cat")
    res = cursor.fetchall()
    return render_template("inicio.html",tablas=[res])


## Ver los registros de las tablas

#@app.route('/tabla/<str:nombre>', methods=["GET","POST"])
#def detallejuego(nombre):
#	registros=[]
#
#    connection = pool.acquire()
#    cursor = connection.cursor()
#    cursor.execute("select * from cat")
#    res = cursor.fetchall()
#	
#	for tabla in res:
#        if tabla == str()
#	return render_template("registros.html",registros=registros)

################################################################################


### -Programa principal:

# Este código funciona si se ha ejecutado previamente como usuario startup en la base de datos.
#
if __name__ == '__main__':

    # Iniciar la conexión a la base de datos 
    pool = start_pool()
    # Iniciar la aplicación web
    app.run(port=int(os.environ.get('PORT', '8080')))

