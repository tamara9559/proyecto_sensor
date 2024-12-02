!bienvenido al manual de usuario!

Cómo Usar el Sistema
1. Iniciar el Servidor
Antes de utilizar la interfaz web, asegúrate de que el servidor de la API y el simulador de sensores estén en funcionamiento:

API:
El servidor Flask debe estar en ejecución para que la interfaz web pueda acceder a los datos de la base de datos, para ejecutarlo debes ingresar el siguiente comando para que se inicie "python api_app.py" importarte estar ubicado en el directorio "proyecto sensores\web_app" ya que aqui se encuentra la api.

Simulador de Sensores:
El simulador generará datos de temperatura automáticamente y los enviará al servidor cada 5 segundos, para iniciarlo en el terminal colocaras el siguiente comando "python simuladorCongelador.py" importante que estes en el directorio "proyecto sensores\simulador" ya que aqui se encuentra el simulador.

Base de Datos:
esta base de datos esta siempre disponible y con las credenciales se accede de forma automatica y no necesita intervencion del usuario

interfaz web:
para acceder a la interfaz donde encontraras los datos recopilados en la BD accedes al siguiente link: http://127.0.0.1:5000

Consultar Datos de Sensores
Seleccionar Sensor:
En el formulario, selecciona un sensor de la lista disponible.
Seleccionar Rango de Fecha y Hora:
Elige el rango de fecha y hora para los cuales deseas ver los datos. Esto te permitirá filtrar los registros específicos de esa selección.
Ver Datos:
Haz clic en el botón de "Consultar Datos". Los datos correspondientes se mostrarán en una tabla en la misma página.
Ver Gráficos:
Los datos de temperatura también se mostrarán en gráficos interactivos generados por Chart.js, lo que te permitirá visualizar las tendencias de temperatura a lo largo del tiempo.


