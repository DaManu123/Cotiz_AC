// JavaScript para Nueva Cotización

let lineaContador = 0;

$(document).ready(function() {
    // Cargar número consecutivo
    cargarConsecutivo();
    
    // Establecer fecha actual
    $('#fecha').val(obtenerFechaActual());
    
    // Cargar clientes
    cargarClientesSelect('cliente-id');
    
    // Agregar primera línea
    agregarLinea();
    
    // Submit del formulario
    $('#form-cotizacion').on('submit', function(e) {
        e.preventDefault();
        guardarCotizacion();
    });
});

function cargarConsecutivo() {
    $.get('/api/cotizaciones/consecutivo', function(data) {
        $('#numero-cotizacion').val(data.numero_cotizacion);
    });
}

function agregarLinea() {
    lineaContador++;
    const nuevaLinea = `
        <tr data-linea="${lineaContador}">
            <td>
                <input type="number" class="form-control cantidad" step="0.01" min="0" value="1" required>
            </td>
            <td>
                <textarea class="form-control descripcion" rows="2" required></textarea>
            </td>
            <td>
                <input type="number" class="form-control precio-unitario" step="0.01" min="0" value="0" required>
            </td>
            <td>
                <input type="text" class="form-control total-linea currency-input" readonly value="$0.00">
            </td>
            <td class="text-center">
                <button type="button" class="btn btn-sm btn-danger" onclick="eliminarLinea(${lineaContador})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>
    `;
    
    $('#conceptos-body').append(nuevaLinea);
    
    // Eventos para calcular totales
    $(`tr[data-linea="${lineaContador}"] .cantidad, tr[data-linea="${lineaContador}"] .precio-unitario`).on('input', function() {
        calcularLineaTotal($(this).closest('tr'));
        calcularTotales();
    });
}

function eliminarLinea(lineaId) {
    if ($('#conceptos-body tr').length === 1) {
        mostrarNotificacion('Debe haber al menos una línea de concepto', 'warning');
        return;
    }
    
    $(`tr[data-linea="${lineaId}"]`).remove();
    calcularTotales();
}

function calcularLineaTotal($linea) {
    const cantidad = parseFloat($linea.find('.cantidad').val()) || 0;
    const precioUnitario = parseFloat($linea.find('.precio-unitario').val()) || 0;
    const total = cantidad * precioUnitario;
    
    $linea.find('.total-linea').val(formatearMoneda(total));
}

function calcularTotales() {
    let subtotal = 0;
    
    $('#conceptos-body tr').each(function() {
        const cantidad = parseFloat($(this).find('.cantidad').val()) || 0;
        const precioUnitario = parseFloat($(this).find('.precio-unitario').val()) || 0;
        subtotal += cantidad * precioUnitario;
    });
    
    const impuestos = subtotal * 0.16; // IVA 16%
    const total = subtotal + impuestos;
    
    $('#subtotal').text(formatearMoneda(subtotal));
    $('#impuestos').text(formatearMoneda(impuestos));
    $('#total').text(formatearMoneda(total));
}

function guardarCotizacion() {
    // Validar cliente
    const clienteId = $('#cliente-id').val();
    if (!clienteId) {
        mostrarNotificacion('Debe seleccionar un cliente', 'warning');
        $('#cliente-id').focus();
        return;
    }
    
    // Validar que haya al menos una línea
    if ($('#conceptos-body tr').length === 0) {
        mostrarNotificacion('Debe agregar al menos un concepto', 'warning');
        return;
    }
    
    // Recopilar detalles
    const detalles = [];
    let detallesValidos = true;
    
    $('#conceptos-body tr').each(function() {
        const cantidad = parseFloat($(this).find('.cantidad').val());
        const descripcion = $(this).find('.descripcion').val().trim();
        const precioUnitario = parseFloat($(this).find('.precio-unitario').val());
        
        if (!cantidad || !descripcion || !precioUnitario) {
            detallesValidos = false;
            return false; // break
        }
        
        detalles.push({
            cantidad: cantidad,
            descripcion: descripcion,
            precio_unitario: precioUnitario
        });
    });
    
    if (!detallesValidos) {
        mostrarNotificacion('Complete todos los campos de los conceptos', 'warning');
        return;
    }
    
    // Preparar datos
    const data = {
        cliente_id: parseInt(clienteId),
        fecha: $('#fecha').val(),
        estatus: $('#estatus').val(),
        notas: $('#notas').val(),
        detalles: detalles
    };
    
    // Deshabilitar botón
    const btnGuardar = $('button[type="submit"]');
    deshabilitarBoton(btnGuardar, 'Guardando...');
    
    // Enviar al servidor
    $.ajax({
        url: '/api/cotizaciones',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            habilitarBoton(btnGuardar);
            mostrarNotificacion('Cotización guardada exitosamente', 'success');
            
            // Preguntar si desea ver la cotización o crear una nueva
            setTimeout(() => {
                if (confirm('¿Desea descargar la cotización en PDF?')) {
                    window.location.href = `/api/cotizaciones/${response.cotizacion.id}/export/pdf`;
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                } else {
                    window.location.href = '/';
                }
            }, 1000);
        },
        error: function(error) {
            habilitarBoton(btnGuardar);
            manejarErrorAPI(error);
        }
    });
}

function guardarNuevoCliente() {
    const nombre = $('#nuevo-nombre').val().trim();
    
    if (!nombre) {
        mostrarNotificacion('El nombre es requerido', 'warning');
        return;
    }
    
    const data = {
        nombre: nombre,
        telefono: $('#nuevo-telefono').val(),
        email: $('#nuevo-email').val(),
        direccion: $('#nuevo-direccion').val()
    };
    
    $.ajax({
        url: '/api/clientes',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            mostrarNotificacion('Cliente creado exitosamente', 'success');
            
            // Cerrar modal
            $('#modalNuevoCliente').modal('hide');
            
            // Limpiar formulario
            $('#form-nuevo-cliente')[0].reset();
            
            // Recargar lista de clientes y seleccionar el nuevo
            cargarClientesSelect('cliente-id', response.cliente.id);
        },
        error: function(error) {
            manejarErrorAPI(error);
        }
    });
}
