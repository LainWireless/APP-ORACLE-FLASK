# Aplicación Web para Oracle

# Importamos las funciones del sistema, el módulo que conecta python con oracle y flask para la aplicación en cuestión.
import os
import sys
import cx_Oracle
from flask import Flask, render_template, abort,request
from flask import Flask
app = Flask(__name__)

# Crear un formulario que sirva como login para la base de datos de oracle en la que vamos a trabajar.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Recogemos los datos del formulario
        usuario = request.form['usuario']
        password = request.form['password']
        # Conectamos con la base de datos
        con = cx_Oracle.connect(usuario, password, 'localhost/ORCLCDB')
        # Creamos un cursor para ejecutar las consultas
        cur = con.cursor()
        # Ejecutamos la consulta
        cur.execute("SELECT * FROM EMPLEADOS")
        # Recogemos los datos de la consulta
        datos = cur.fetchall()
        # Cerramos la conexión
        con.close()
        # Devolvemos los datos
        return render_template('index.html', datos=datos)
    return render_template('login.html')

# Creamos una ruta para la página principal en la cual se nos mostrarán todas las tablas de la base de datos. 
@app.route('/')
def index():
    return render_template('index.html')

# Creamos una ruta para la página de error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# Iniciar la aplicación web
if __name__ == '__main__':
    app.run(debug=True)