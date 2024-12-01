import time
import random
import requests
from datetime import datetime

def simulador_congelador(api_url):
    try:
        while True:
            # Generar una temperatura aleatoria entre -20°C y -18°C
            temperatura = round(random.uniform(-20, -18), 2)
            idsensor = "JDTE5847"  # ID fijo del sensor
            print(f"Sensor de temperatura {idsensor} - Temperatura actual: {temperatura}°C")

            # Obtener la fecha y hora actuales
            now = datetime.now()
            fecha = now.strftime("%Y-%m-%d")
            hora = now.strftime("%H:%M:%S")
            
            # Enviar datos a la API, incluyendo fecha y hora
            payload = {
                "idsensor": idsensor,
                "fecha": fecha,
                "hora": hora,
                "temperatura": temperatura
            }
            
            response = requests.post(api_url, json=payload)

            # Imprimir respuesta de la API
            print(f"API respondió: {response.status_code} - {response.text}")
            
            # Esperar 5 segundos antes de generar la siguiente lectura
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nSimulación detenida.")
    except Exception as e:
        print(f"Error durante la simulación: {e}")

# Ejecutar el simulador
if __name__ == "__main__":
    # URL de la API
    API_URL = "http://127.0.0.1:5000/api/datos"  # Cambiar si la API está en otro lugar
    simulador_congelador(API_URL)
