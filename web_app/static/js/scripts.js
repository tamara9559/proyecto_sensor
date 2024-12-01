// Manejar el formulario para mostrar datos
$("#sensorForm").submit(function (event) {
    event.preventDefault();

    const sensor_id = $("#sensor_id").val();
    const fecha = $("#fecha").val();

    // Validar que los campos requeridos estén presentes
    if (!sensor_id || !fecha) {
        alert("Por favor selecciona un sensor y una fecha.");
        return;
    }

    // Crear un objeto para los datos que vamos a enviar
    const dataToSend = { idsensor: sensor_id, fecha: fecha };

    // Solicitar datos del sensor y la fecha seleccionados
    $.ajax({
        url: "/api/datos",
        method: "GET",
        data: dataToSend,
        success: function (data) {
            // Ordenar los datos por la hora (formato HH:MM:SS)
            data.sort((a, b) => a.hora.localeCompare(b.hora));

            // Limpiar la tabla antes de agregar nuevos datos
            const tbody = $("#tabla-datos tbody");
            tbody.empty();

            if (data.length === 0) {
                alert("No se encontraron datos para la fecha seleccionada.");
            } else {
                // Actualizar la tabla con los datos obtenidos
                data.forEach(function (dato) {
                    tbody.append(
                        "<tr>" +
                        "<td>" + dato.idsensor + "</td>" +
                        "<td>" + dato.fecha + "</td>" +
                        "<td>" + dato.hora + "</td>" +
                        "<td>" + dato.temperatura + "</td>" +
                        "</tr>"
                    );
                });

                // Generar el gráfico con los datos ordenados
                const ctx = document.getElementById("grafico").getContext("2d");
                new Chart(ctx, {
                    type: "line",
                    data: {
                        labels: data.map(d => d.hora),  // Eje X: horas
                        datasets: [{
                            label: "Temperatura",
                            data: data.map(d => d.temperatura),  // Eje Y: temperaturas
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
