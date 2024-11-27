from flask import Flask, request, jsonify, render_template
from DB import DB

app = Flask(__name__)

# Inicializar BD
SERVICE_ACCOUNT_PATH = "credenciales/firebase_proyecto.json"
COLLECTION_NAME = "sensor"
db = DB(SERVICE_ACCOUNT_PATH, COLLECTION_NAME)


@app.route("/")
def index():
    """
    Renderiza la página principal.
    """
    return render_template("index.html")

@app.route("/api/sensores", methods=["GET"])
def obtener_sensores():
    """
    Endpoint para obtener una lista única de sensores disponibles.
    """
    try:
        # Obtener los documentos de la colección "sensor"
        sensores = db.db.collection("sensor").stream()

        # Extraer valores únicos de `idsensor`
        sensores_data = set()
        for sensor in sensores:
            data = sensor.to_dict()
            if "idsensor" in data:
                sensores_data.add(data["idsensor"])  # Usar un conjunto para evitar duplicados

        # Convertir el conjunto en una lista para enviarlo como JSON
        sensores_unicos = [{"id": idsensor} for idsensor in sensores_data]

        return jsonify({"sensores": sensores_unicos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/api/datos", methods=["GET"])
def obtener_datos():
    """
    Endpoint para obtener los datos de un sensor en una fecha (y hora) específica.
    """
    try:
        sensor_id = request.args.get('idsensor')
        fecha = request.args.get('fecha')
        hora = request.args.get('hora')  # Hora opcional

        if not sensor_id or not fecha:
            return jsonify({"error": "Se requiere 'idsensor' y 'fecha'."}), 400

        # Consulta inicial por fecha y sensor
        query = db.db.collection("sensor")\
            .where("idsensor", "==", sensor_id)\
            .where("fecha", "==", fecha)

        # Si se proporciona una hora, añadir filtro
        if hora:
            query = query.where("hora", "==", hora)

        # Ejecutar la consulta
        datos = query.stream()

        datos_resultados = [{
            "idsensor": dato.get("idsensor"),
            "fecha": dato.get("fecha"),
            "hora": dato.get("hora"),
            "temperatura": dato.get("temperatura")
        } for dato in datos]

        return jsonify({"datos": datos_resultados}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/api/datos", methods=["POST"])
def recibir_datos():
    """
    Endpoint para recibir datos del sensor.
    """
    try:
        # Obtener datos enviados por el cliente (simulador)
        datos = request.get_json()
        
        # Validar que los campos requeridos estén presentes
        if not datos or "idsensor" not in datos or "temperatura" not in datos:
            return jsonify({"error": "Datos inválidos. Se requiere 'idsensor' y 'temperatura'."}), 400

        idsensor = datos["idsensor"]
        temperatura = datos["temperatura"]

        # Validar tipo de datos
        if not isinstance(idsensor, str) or not isinstance(temperatura, (int, float)):
            return jsonify({"error": "Tipos de datos inválidos."}), 400

        # Registrar el dato en Firebase
        doc_id = db.agregar_dato(idsensor, temperatura)

        # Respuesta exitosa
        return jsonify({"mensaje": "Dato registrado correctamente.", "id": doc_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Ejecutar la API en modo desarrollo
    app.run(debug=True)
