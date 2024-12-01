from flask import Flask, request, jsonify, render_template
from google.cloud import firestore
import os

# Inicialización de Flask
app = Flask(__name__)

# Configurar el archivo de credenciales de Firebase
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciales/firebase_proyecto.json"

# Conexión a Firestore
db = firestore.Client()
collection_name = "sensores"  # Nombre de la colección en Firestore

# Ruta principal (Renderiza la página HTML principal)
@app.route('/')
def index():
    return render_template("index.html")

# Ruta para obtener sensores únicos
@app.route('/api/sensores', methods=['GET'])
def obtener_sensores():
    try:
        # Consultar Firestore para obtener los sensores únicos
        sensores_ref = db.collection(collection_name)
        sensores_docs = sensores_ref.stream()

        sensores_unicos = set(doc.to_dict().get("idsensor") for doc in sensores_docs)
        sensores_unicos = list(filter(None, sensores_unicos))  # Eliminar valores nulos o vacíos

        return jsonify(sensores_unicos), 200
    except Exception as e:
        print(f"Error en la API: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para registrar datos de sensores (POST)
@app.route('/api/datos', methods=['POST'])
def registrar_datos():
    try:
        # Obtener datos enviados en el cuerpo de la solicitud
        datos = request.json

        # Validar datos obligatorios
        if not all(k in datos for k in ("idsensor", "fecha", "hora", "temperatura")):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        # Insertar los datos en Firestore
        db.collection(collection_name).add(datos)
        return jsonify({"message": "Dato registrado exitosamente"}), 201
    except Exception as e:
        print(f"Error en la API: {e}")
        return jsonify({"error": str(e)}), 500

# Ruta para obtener datos filtrados (GET)
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    try:
        # Obtener parámetros de consulta
        idsensor = request.args.get('idsensor')
        fecha = request.args.get('fecha')

        # Consulta inicial a la colección
        query = db.collection(collection_name)

        # Aplicar filtros correctamente con argumentos posicionales
        if idsensor:
            query = query.where("idsensor", "==", idsensor)
        if fecha:
            query = query.where("fecha", "==", fecha)

        # Ordenar los resultados por hora
        query = query.order_by("hora", direction=firestore.Query.ASCENDING)

        # Ejecutar la consulta
        docs = query.stream()
        resultados = [doc.to_dict() for doc in docs]

        # Verificar si hay datos
        if not resultados:
            return jsonify({"message": "No se encontraron datos para los filtros aplicados"}), 200

        return jsonify(resultados), 200

    except Exception as e:
        print(f"Error en la API: {e}")
        return jsonify({"error": str(e)}), 500

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
