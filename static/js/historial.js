// JavaScript para Historial de Cotizaciones

$(document).ready(function() {
    cargarClientesSelect('filtro-cliente');
    cargarHistorial();
});

function aplicarFiltros() {
    cargarHistorial();
}

function cargarHistorial() {
    // Construir parámetros de filtro
    const params = {};
    
    if ($('#filtro-cliente').val()) {
        params.cliente_id = $('#filtro-cliente').val();
    }
    if ($('#filtro-estatus').val()) {
        params.estatus = $('#filtro-estatus').val();
    }
    if ($('#filtro-fecha-desde').val()) {
        params.fecha_desde = $('#filtro-fecha-desde').val();
    }
    if ($('#filtro-fecha-hasta').val()) {
        params.fecha_hasta = $('#filtro-fecha-hasta').val();
    }
    
    // Cargar cotizaciones
    $.get('/api/cotizaciones', params, function(data) {
        const tbody = $('#tabla-historial tbody');
        tbody.empty();
        
        $('#total-resultados').text(`${data.total} resultados`);
        
        if (data.cotizaciones.length === 0) {
            tbody.append(`
                <tr>
                    <td colspan="8" class="text-center text-muted">
                        No hay cotizaciones que coincidan con los filtros
                    </td>
                </tr>
            `);
            return;
        }
        
        data.cotizaciones.forEach(function(cot) {
            const estatusBadge = getEstatusBadge(cot.estatus);
            tbody.append(`
                <tr>
                    <td><strong>${cot.numero_cotizacion}</strong></td>
                    <td>${formatearFecha(cot.fecha)}</td>
                    <td>${cot.cliente.nombre}</td>
                    <td>$${formatearMonto(cot.subtotal)}</td>
                    <td>$${formatearMonto(cot.impuestos)}</td>
                    <td><strong>$${formatearMonto(cot.total)}</strong></td>
                    <td>${estatusBadge}</td>
                    <td>
                        <div class="btn-group btn-group-sm" role="group">
                            <button class="btn btn-outline-primary" onclick="verDetalle(${cot.id})" title="Ver detalle">
                                <i class="bi bi-eye"></i>
                            </button>
                            <a href="/api/cotizaciones/${cot.id}/export/pdf" class="btn btn-outline-danger" title="PDF">
                                <i class="bi bi-file-pdf"></i>
                            </a>
                            <a href="/api/cotizaciones/${cot.id}/export/excel" class="btn btn-outline-success" title="Excel">
                                <i class="bi bi-file-excel"></i>
                            </a>
                            <button class="btn btn-outline-danger" onclick="eliminarCotizacion(${cot.id})" title="Eliminar">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `);
        });
    });
}

function verDetalle(cotizacionId) {
    $.get(`/api/cotizaciones/${cotizacionId}`, function(data) {
        const cot = data.cotizacion;
        
        let detallesHTML = '';
        cot.detalles.forEach(function(detalle) {
            detallesHTML += `
                <tr>
                    <td class="text-center">${detalle.cantidad}</td>
                    <td>${detalle.descripcion}</td>
                    <td class="text-end">$${formatearMonto(detalle.precio_unitario)}</td>
                    <td class="text-end"><strong>$${formatearMonto(detalle.total_linea)}</strong></td>
                </tr>
            `;
        });
        
        const html = `
            <div class="row mb-3">
                <div class="col-md-6">
                    <h6 class="text-primary">Información de Cotización</h6>
                    <p><strong>No. Cotización:</strong> ${cot.numero_cotizacion}</p>
                    <p><strong>Fecha:</strong> ${formatearFecha(cot.fecha)}</p>
                    <p><strong>Estatus:</strong> ${getEstatusBadge(cot.estatus)}</p>
                </div>
                <div class="col-md-6">
                    <h6 class="text-info">Cliente</h6>
                    <p><strong>Nombre:</strong> ${cot.cliente.nombre}</p>
                    <p><strong>Teléfono:</strong> ${cot.cliente.telefono || '-'}</p>
                    <p><strong>Email:</strong> ${cot.cliente.email || '-'}</p>
                </div>
            </div>
            
            <h6 class="text-success mb-3">Conceptos</h6>
            <div class="table-responsive mb-3">
                <table class="table table-bordered table-sm">
                    <thead class="table-light">
                        <tr>
                            <th style="width: 10%;">Cant.</th>
                            <th style="width: 50%;">Descripción</th>
                            <th style="width: 20%;">Precio Unit.</th>
                            <th style="width: 20%;">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${detallesHTML}
                    </tbody>
                </table>
            </div>
            
            <div class="row">
                <div class="col-md-8">
                    ${cot.notas ? `
                        <h6>Notas</h6>
                        <p class="text-muted">${cot.notas}</p>
                    ` : ''}
                </div>
                <div class="col-md-4">
                    <table class="table table-sm">
                        <tr>
                            <td class="text-end"><strong>Subtotal:</strong></td>
                            <td class="text-end">$${formatearMonto(cot.subtotal)}</td>
                        </tr>
                        <tr>
                            <td class="text-end"><strong>IVA (16%):</strong></td>
                            <td class="text-end">$${formatearMonto(cot.impuestos)}</td>
                        </tr>
                        <tr class="table-success">
                            <td class="text-end"><strong>TOTAL:</strong></td>
                            <td class="text-end"><strong>$${formatearMonto(cot.total)}</strong></td>
                        </tr>
                    </table>
                </div>
            </div>
        `;
        
        $('#detalle-content').html(html);
        $('#modalDetalle').modal('show');
    });
}

function eliminarCotizacion(cotizacionId) {
    confirmarAccion('¿Está seguro de eliminar esta cotización?\nEsta acción no se puede deshacer.', function() {
        $.ajax({
            url: `/api/cotizaciones/${cotizacionId}`,
            method: 'DELETE',
            success: function() {
                mostrarNotificacion('Cotización eliminada exitosamente', 'success');
                cargarHistorial();
            },
            error: function(error) {
                manejarErrorAPI(error);
            }
        });
    });
}
