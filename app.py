from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"http://localhost:8000"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:15sigo21@localhost:5432/mi_base_de_datos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Jugador (db.Model):
    __tablename__ = "jugadores"
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)    
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    equipo = db.Column(db.String(50), nullable=False)
    posicion = db.Column(db.String(50), nullable=False)
    nacionalidad = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(200), nullable=False)

class Mundial (db.Model):
    __tablename__ = "mundiales"
    id = db.Column(db.Integer, primary_key=True)
    año = db.Column(db.Integer, nullable=False)
    sede = db.Column(db.String(50), nullable=False)
    pais_campeon = db.Column(db.String(50), nullable=False) 


def contar_mundiales_por_nacionalidad(jugador_id):
    jugador = Jugador.query.get(jugador_id)
    if jugador is None:
        return f"Jugador con ID {jugador_id} no encontrado, podés generarlo si querés..."
    nacionalidad = jugador.nacionalidad
    conteo_mundiales = Mundial.query.filter_by(pais_campeon=nacionalidad).count()
    return conteo_mundiales

if __name__ == '__main__':
    with app.app_context():
        jugador_id = 1  
        print(contar_mundiales_por_nacionalidad(jugador_id))


@app.route("/", methods=["GET"])
def hola():
    return send_from_directory('templates', 'index.html')

@app.route("/jugadores/<int:id>", methods=["GET"])
def get_jugador(id):
    jugador = Jugador.query.get(id)
    if jugador is None:
        return jsonify({"error": f"Jugador con ID {id} no encontrado."}), 404

    jugador_info = {
        "id": jugador.id,
        "nombre": jugador.nombre,
        "edad": jugador.edad,
        "equipo": jugador.equipo,
        "posicion": jugador.posicion,
        "nacionalidad": jugador.nacionalidad,
        "imagen": jugador.imagen,
        "mundiales_ganados": contar_mundiales_por_nacionalidad(jugador.id)
    }

    return jsonify(jugador_info)

@app.route("/jugadores", methods=["GET"])
def todos_los_jugadores():
    jugadores = Jugador.query.all()
    jugadores_info = []
    for jugador in jugadores:
        jugadores_info.append({
            "id": jugador.id,
            "nombre": jugador.nombre,
            "edad": jugador.edad,
            "equipo": jugador.equipo,
            "posicion": jugador.posicion,
            "nacionalidad": jugador.nacionalidad,
            "imagen": jugador.imagen
        })
    return jsonify(jugadores_info)

@app.route("/mundiales", methods=["GET"])
def get_mundiales():
    mundiales = Mundial.query.all()
    mundiales_info = []
    for mundial in mundiales:
        mundiales_info.append({
            "id": mundial.id,
            "año": mundial.año,
            "sede": mundial.sede,
            "pais_campeon": mundial.pais_campeon
        })
    return jsonify(mundiales_info)



@app.route("/nuevojugador", methods=["POST"])
def nuevo_jugador():
    try:
        data = request.json
        print(f"Datos recibidos: {data}")

        nuevo_nombre = data.get('nombre')
        nueva_edad = data.get('edad')
        nueva_nacionalidad = data.get('nacionalidad')
        nueva_posicion = data.get('posicion')
        nuevo_equipo = data.get('equipo')
        nueva_imagen = data.get('imagen')

        if not all([nuevo_nombre, nueva_edad, nueva_nacionalidad, nueva_posicion, nuevo_equipo, nueva_imagen]):
            return jsonify({'mensaje': 'Todos los campos son obligatorios'}), 400

        nuevo_jugador = Jugador(
            nombre=nuevo_nombre, 
            edad=nueva_edad, 
            nacionalidad=nueva_nacionalidad, 
            posicion=nueva_posicion, 
            equipo=nuevo_equipo, 
            imagen=nueva_imagen
        )
        db.session.add(nuevo_jugador)
        db.session.commit()
        return jsonify({'jugador': {
            'id': nuevo_jugador.id, 
            'nombre': nuevo_jugador.nombre, 
            'edad': nuevo_jugador.edad, 
            'nacionalidad': nuevo_jugador.nacionalidad, 
            'posicion': nuevo_jugador.posicion, 
            'equipo': nuevo_jugador.equipo, 
            'imagen': nuevo_jugador.imagen
        }}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'mensaje': 'No se pudo crear el nuevo jugador', 'error': str(e)}), 500



@app.route("/jugadores/<int:id>", methods=["DELETE"])
def eliminar_jugador(id):
    try:
        jugador = Jugador.query.get(id)
        if jugador is None:
            return jsonify({"success": False, "error": f"Jugador con ID {id} no encontrado."}), 404
        
        db.session.delete(jugador)
        db.session.commit()
        return jsonify({"success": True, "mensaje": f"Jugador con ID {id} eliminado con éxito."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "mensaje": "No se pudo eliminar el jugador", "error": str(e)}), 500


@app.route("/jugador/<int:id>", methods=["PUT"])
def actualizar_jugador(id):
    try:
        jugador = Jugador.query.get(id)
        if jugador is None:
            return jsonify({"error": f"Jugador con ID {id} no encontrado."}), 404

        data = request.json
        jugador.nombre = data.get('nombre', jugador.nombre)
        jugador.edad = data.get('edad', jugador.edad)
        jugador.nacionalidad = data.get('nacionalidad', jugador.nacionalidad)
        jugador.posicion = data.get('posicion', jugador.posicion)
        jugador.equipo = data.get('equipo', jugador.equipo)
        jugador.imagen = data.get('imagen', jugador.imagen)

        db.session.commit()

        return jsonify({"success": True, 'jugador': {
            'id': jugador.id,
            'nombre': jugador.nombre,
            'edad': jugador.edad,
            'nacionalidad': jugador.nacionalidad,
            'posicion': jugador.posicion,
            'equipo': jugador.equipo,
            'imagen': jugador.imagen
        }}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'mensaje': 'No se pudo actualizar el jugador', 'error': str(e)}), 500

if __name__== '__main__':
    with app.app_context():
       db.create_all()
    app.run
