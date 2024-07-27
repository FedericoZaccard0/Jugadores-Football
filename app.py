
from flask import Flask, request, send_file, jsonify, abort
from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"http://localhost:8000"}})

jugadores= [
        {
            "nombre": "Lionel Messi",
            "id": " 1",
            "edad": "36",
            "equipo": "Inter Miami CF",
            "posicion": "Delantero",
            "nacionalidad": "Argentina",
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg/220px-Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg"
        },
        {
            "nombre": "Cristiano Ronaldo",
            "id": " 2",
            "edad": "39",
            "equipo": "Al-Nassr",
            "posicion": "Delantero",
            "nacionalidad": "Portugal",
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Cristiano_Ronaldo_playing_for_Al_Nassr_FC_against_Persepolis%2C_September_2023_%28cropped%29.jpg/220px-Cristiano_Ronaldo_playing_for_Al_Nassr_FC_against_Persepolis%2C_September_2023_%28cropped%29.jpg"
        },
        {
            "nombre": "Neymar Jr.",
            "id": " 3",
            "edad": "32",
            "equipo": "Al-Hilal",
            "posicion": "Delantero",
            "nacionalidad": "Brasil",
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Bra-Cos_%281%29_%28cropped%29.jpg/225px-Bra-Cos_%281%29_%28cropped%29.jpg"
        },
        {
            "nombre": "Kevin De Bruyne",
            "id": " 4",
            "edad": "32",
            "equipo": "Manchester City",
            "posicion": "Centrocampista",
            "nacionalidad": "Bélgica",
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/2021-12-07_Fu%C3%9Fball%2C_M%C3%A4nner%2C_UEFA_Champions_League%2C_RB_Leipzig_-_Manchester_City_FC_1DX_2782_by_Stepro_%28cropped%29.jpg/220px-2021-12-07_Fu%C3%9Fball%2C_M%C3%A4nner%2C_UEFA_Champions_League%2C_RB_Leipzig_-_Manchester_City_FC_1DX_2782_by_Stepro_%28cropped%29.jpg"
        },
        {
            "nombre": "Kylian Mbappé",
            "id": " 5",
            "edad": "25",
            "equipo": "Paris Saint-Germain",
            "posicion": "Delantero",
            "nacionalidad": "Francia",
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/2022_FIFA_World_Cup_France_4%E2%80%931_Australia_-_%287%29_%28cropped%29.jpg/220px-2022_FIFA_World_Cup_France_4%E2%80%931_Australia_-_%287%29_%28cropped%29.jpg"
        },
        {
            "nombre": "Robert Lewandowski",
            "id": " 6",
            "edad": "35",
            "equipo": "Barcelona",
            "posicion": "Delantero",
            "nacionalidad": "Polonia",
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/2019147195017_2019-05-27_Fussball_1.FC_Kaiserslautern_vs_FC_Bayern_M%C3%BCnchen_-_Sven_-_1D_X_MK_II_-_2036_-_B70I0336.jpg/200px-2019147195017_2019-05-27_Fussball_1.FC_Kaiserslautern_vs_FC_Bayern_M%C3%BCnchen_-_Sven_-_1D_X_MK_II_-_2036_-_B70I0336.jpg"
        },
        {
            "nombre": "Mohamed Salah",
            "id": " 7",
            "edad": "32",
            "equipo": "Liverpool",
            "posicion": "Delantero",
            "nacionalidad": "Egipto",
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Mohamed_Salah_2021_CAN_Final.jpg/250px-Mohamed_Salah_2021_CAN_Final.jpg"
        },
        {
            "nombre": "Luka Modrić",
            "id": " 8",
            "edad": "38",
            "equipo": "Real Madrid",
            "posicion": "Centrocampista",
            "nacionalidad": "Croacia",
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Shahter-Reak_M_2015_%2810%29.jpg/170px-Shahter-Reak_M_2015_%2810%29.jpg"
        },
        {
            "nombre": "Virgil van Dijk",
            "id": " 9",
            "edad": "32",
            "equipo": "Liverpool",
            "posicion": "Defensor",
            "nacionalidad": "Países Bajos",
            "imagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Virgil_van_Dijk_2015.jpg/170px-Virgil_van_Dijk_2015.jpg"
        },
        {
            "nombre": "Erling Haaland",
            "id": " 10",
            "edad": "23",
            "equipo": "Manchester City",
            "posicion": "Delantero",
            "nacionalidad": "Noruega",
            "imagen": "https://media.discordapp.net/attachments/1220137698904248420/1266252332786778143/170px-Erling_Haaland_2020.png?ex=66a478e1&is=66a32761&hm=474dfadc1fb3e28bbad551a552e70c8452adae7c0fcd6898b64c23d312211116&=&format=webp&quality=lossless"
        },
    ]



@app.route("/jugadores/<id>")
@cross_origin()
def get_jugador(id):
    # Buscar el jugador por ID
    for jugador in jugadores:
        if jugador["id"].strip() == id.strip():
            return jsonify(jugador)
    # Si no se encuentra, devolver un error 404
    return jsonify({"error": "Jugador no encontrado"}), 404


def get_character_by_id(id):
    for jugador in jugadores:                      
        if jugador["id"] == str(id):
            return jugador


@app.route("/jugadores")
@cross_origin()
def home():
    return jsonify(jugadores)

def remove_character(id):
    global jugadores
    jugadores = [jugador for jugador in jugadores if jugador["id"] != id]


@app.route("/jugadores/<id>", methods = ["DELETE"])
@cross_origin()
def remover_jugador_por_id(id):
    if get_character_by_id(id) is None:
        return {"success": False }
    remove_character(id)
    return {"success": True}


ultimo_id=int(max(jugador["id"] for jugador in jugadores)) if jugadores else 0
ultimo_id=ultimo_id +1
@app.route("/nuevojugador", methods= ["POST"])
def crear_jugador():
    global ultimo_id
    global jugadores
    
    data = request.get_json()
    nombre = data.get("nombre")
    edad = data.get("edad")
    nacion = data.get("nacion")
    posicion = data.get("posicion")
    equipo = data.get("equipo")
    imagen = data.get("imagen")
    ultimo_id+=1
    nuevo_id= int(ultimo_id)

    jugador= { "nombre": nombre,
            "id":  f" {nuevo_id}",
            "edad": edad,
            "equipo": equipo,
            "posicion": posicion,
            "nacionalidad": nacion,
            "imagen": imagen,
            }
    jugadores.append(jugador)
    return jsonify({"success": True, "jugador": jugador})




if __name__ == "__main__":
    app.run(debug=True)



