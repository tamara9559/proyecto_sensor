import time
import random
import requests

def simulador_congelador(api_url):
    try:
        while True:
            # Generar una temperatura aleatoria entre -20°C y -18°C
            temperatura = round(random.uniform(-20, -18), 2)
            idsensor = "JDTE5847"  # ID fijo del sensor
            print(f"Sensor de temperatura {idsensor} - Temperatura actual: {temperatura}°C")
            
            # Enviar datos a la API
            payload = {"idsensor": idsensor, "temperatura": temperatura}  # Cambié "valor" por "temperatura"
            response = requests.post(api_url, json=payload)

            # Imprimir respuesta de la API
            print(f"API respondió: {response.status_code} - {response.text}")
            
            # Esperar 3 segundos antes de generar la siguiente lectura
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nSimulación detenida.")
    except Exception as e:
        print(f"Error durante la simulación: {e}")


# Ejecutar el simulador
if __name__ == "__main__":
    # URL de la API
    API_URL = "http://127.0.0.1:5000/api/datos"  # Cambiar si la API está en otro lugar
    simulador_congelador(API_URL)
