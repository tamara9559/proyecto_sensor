// Manejo del formulario para mostrar datos
$("#sensorForm").submit(function (event) {
    // Previene el comportamiento por defecto del formulario (recarga de la página)
    event.preventDefault();

    // Obtiene el valor seleccionado para el sensor y la fecha
    const sensor_id = $("#sensor_id").val();
    const fecha = $("#fecha").val();

    // Verifica que los campos requeridos no estén vacíos
    if (!sensor_id || !fecha) {
        alert("Por favor selecciona un sensor y una fecha.");
        return;
    }

    // Crea un objeto con los datos a enviar a la API
    const dataToSend = { idsensor: sensor_id, fecha: fecha };

    // Solicita los datos a la API con una solicitud GET
    $.ajax({
        url: "/api/datos",  // URL del endpoint de la API
        method: "GET",  // Método HTTP utilizado para la solicitud
        data: dataToSend,  // Datos a enviar (sensor y fecha)
        success: function (data) {
            // Si la solicitud es exitosa, se procesa la respuesta

            // Ordena los datos por la hora (en formato HH:MM:SS)
            data.sort((a, b) => a.hora.localeCompare(b.hora));

            // Obtiene el cuerpo de la tabla para insertar los nuevos datos
            const tbody = $("#tabla-datos tbody");
            tbody.empty();  // Limpia la tabla antes de agregar los nuevos datos

            // Si no se encontraron datos para la fecha seleccionada
            if (data.length === 0) {
                alert("No se encontraron datos para la fecha seleccionada.");
            } else {
                // Si se encontraron datos, se agregan a la tabla
                data.forEach(function (dato) {
                    tbody.append(
                        "<tr>" +
                        "<td>" + dato.idsensor + "</td>" +  // Muestra el ID del sensor
                        "<td>" + dato.fecha + "</td>" +  // Muestra la fecha
                        "<td>" + dato.hora + "</td>" +  // Muestra la hora
                        "<td>" + dato.temperatura + "</td>" +  // Muestra la temperatura
                        "</tr>"
                    );
                });

                // Obtiene el contexto del canvas donde se dibujará el gráfico
                const ctx = document.getElementById("grafico").getContext("2d");

                // Crea un nuevo gráfico de tipo "línea" usando los datos obtenidos
                new Chart(ctx, {
                    type: "line",  // Tipo de gráfico (línea)
                    data: {
                        labels: data.map(d => d.hora),  // Etiquetas del eje X (horas)
                        datasets: [{
                            label: "Temperatura",  // Etiqueta de la serie de datos
                            data: data.map(d => d.temperatura),  // Datos del eje Y (temperaturas)
                            borderColor: "rgba(75, 192, 192, 1)",  // Color de la línea
                            fill: false  // No llenar el área debajo de la línea
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                min: -20.5,  // Límite inferior del eje Y (para representar temperaturas de congelador)
                                max: -17.5  // Límite superior del eje Y (para representar temperaturas de congelador)
                            }
                        }
                    }
                });
            }
        },
        error: function () {
            // Si ocurre un error en la solicitud, muestra un mensaje de error
            alert("Error al cargar los datos. Verifica la conexión con la API.");
        }
    });
});
