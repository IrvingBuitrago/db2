from flask import Flask, request, jsonify, render_template
from dml import DML

app = Flask(__name__)

instancia = DML("localhost", "root", "xyz", 3306)

#ruta para el dahsboard
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    if request.method == 'GET':
        # Consultar la lista de usuarios desde la base de datos
        instancia.consultar('SELECT * FROM Users')
        usuarios = instancia.result
        return render_template('usuarios.html', usuarios=usuarios)

# Ruta para mostrar los perfiles
@app.route('/perfiles', methods=['GET'])
def obtener_perfiles():
    if request.method == 'GET':
        # Consultar los perfiles desde la base de datos
        instancia.consultar('SELECT * FROM Profils')
        perfiles = instancia.result
        return render_template('perfiles.html', perfiles=perfiles)

# Ruta para la fidelización
@app.route('/fidelizacion', methods=['GET'])
def fidelizacion():
    # Consultar la vista de puntos acumulados
    instancia.consultar('SELECT first_name, last_name, Total_points FROM AccumlatedPoints')
    fidelizacion_info = instancia.result

    # Consultar las actividades recientes desde la vista
    instancia.consultar('SELECT name_act, date_act FROM RecentActivities')
    actividades_recientes = instancia.result

    return render_template('fidelizacion.html', fidelizacion_info=fidelizacion_info,
                           actividades_recientes=actividades_recientes)

if __name__ == '__main__':
    instancia.conectar()
    app.run(debug=True)