// Manejar el formulario para mostrar datos
$("#sensorForm").submit(function (event) {
    event.preventDefault();

    const sensor_id = $("#sensor_id").val();
    const fecha = $("#fecha").val();
    const hora = $("#hora").val(); // Nueva entrada para buscar por hora

    // Validar que los campos requeridos estén presentes
    if (!sensor_id || !fecha) {
        alert("Por favor selecciona un sensor y una fecha.");
        return;
    }

    // Crear un objeto para los datos que vamos a enviar
    const dataToSend = { idsensor: sensor_id, fecha: fecha };

    // Si la hora está seleccionada, añadirla al objeto
    if (hora) {
        dataToSend.hora = hora;
    }

    // Solicitar datos del sensor, fecha y hora seleccionados
    $.ajax({
        url: "/api/datos",
        method: "GET",
        data: dataToSend,  // Usamos el objeto con los parámetros
        success: function (data) {
            // Limpiar la tabla antes de agregar nuevos datos
            const tbody = $("#tabla-datos tbody");
            tbody.empty();

            if (data.datos.length === 0) {
                alert("No se encontraron datos para la fecha y hora seleccionadas.");
            } else {
                // Actualizar la tabla con los datos obtenidos
                data.datos.forEach(function (dato) {
                    tbody.append(
                        "<tr>" +
                        "<td>" + dato.idsensor + "</td>" +
                        "<td>" + dato.fecha + "</td>" +
                        "<td>" + dato.hora + "</td>" +
                        "<td>" + dato.temperatura + "</td>" +
                        "</tr>"
                    );
                });

                // Generar el gráfico con los datos obtenidos
                const ctx = document.getElementById("grafico").getContext("2d");
                new Chart(ctx, {
                    type: "line",
                    data: {
                        labels: data.datos.map(d => d.hora),  // Eje X: horas
                        datasets: [{
                            label: "Temperatura",
                            data: data.datos.map(d => d.temperatura),  // Eje Y: temperaturas
                            borderColor: "rgba(75, 192, 192, 1)",
                            fill: false
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                min: -20, // Límite inferior
                                max: -17  // Límite superior
                            }
                        }
                    }
                });
            }
        },
        error: function () {
            alert("Error al cargar los datos. Verifica la conexión con la API.");
        }
    });
});
