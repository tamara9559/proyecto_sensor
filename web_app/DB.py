import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime


class DB:
    """
    Clase para manejar operaciones CRUD en una base de datos Firestore.

    Permite agregar, actualizar y eliminar documentos en una colección específica 
    dentro de Firestore, utilizando las credenciales proporcionadas.
    """

    def __init__(self, service_account_path, collection_name):
        """
        Inicializa Firebase y configura la colección principal.

        :param service_account_path: Ruta al archivo de credenciales de servicio JSON para Firebase.
        :param collection_name: Nombre de la colección en Firestore.
        """
        self.collection_name = collection_name
        
        # Inicializa Firebase solo si no ha sido inicializado previamente
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()

    def agregar_dato(self, idsensor, temperatura):
        """
        Agrega un nuevo documento a la colección Firestore. 

        Incluye un campo 'id' generado automáticamente por Firestore 
        y los campos `fecha` y `hora` basados en la hora actual.

        :param idsensor: Identificador del sensor (string).
        :param temperatura: Valor de temperatura registrado por el sensor (float o int).
        :return: ID del documento recién agregado (string).
        """
        fecha_actual = datetime.now()

        # Genera un ID único automáticamente
        doc_ref = self.db.collection(self.collection_name).document()
        auto_id = doc_ref.id  # Obtiene el ID generado automáticamente

        nuevo_dato = {
            "id": auto_id,  # Incluye el ID dentro del documento
            "fecha": fecha_actual.strftime("%Y-%m-%d"),  # Fecha en formato AAAA-MM-DD
            "hora": fecha_actual.strftime("%H:%M:%S"),   # Hora en formato HH:MM:SS
            "idsensor": idsensor,
            "temperatura": temperatura,  # Valor de la medición
        }

        # Guarda el documento en Firestore
        doc_ref.set(nuevo_dato)  # Usamos `set` para asignar datos con el ID generado
        print(f"Documento agregado con ID: {auto_id}")
        return auto_id

    def actualizar_dato(self, doc_id, nuevos_datos):
        """
        Actualiza un documento existente en la colección Firestore.

        :param doc_id: ID del documento a actualizar (string).
        :param nuevos_datos: Diccionario con los campos a actualizar. 
                             Los campos existentes serán reemplazados por los valores nuevos.
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.update(nuevos_datos)
            print(f"Documento con ID {doc_id} actualizado.")
        except Exception as e:
            print(f"Error al actualizar el documento: {e}")

    def eliminar_dato(self, doc_id):
        """
        Elimina un documento de la colección Firestore.

        :param doc_id: ID del documento a eliminar (string).
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.delete()
            print(f"Documento con ID {doc_id} eliminado.")
        except Exception as e:
            print(f"Error al eliminar el documento: {e}")
