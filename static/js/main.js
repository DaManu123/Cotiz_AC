// Funciones globales compartidas

// Formatear fecha para mostrar
function formatearFecha(fecha) {
    if (!fecha) return '';
    const d = new Date(fecha + 'T00:00:00');
    const dia = String(d.getDate()).padStart(2, '0');
    const mes = String(d.getMonth() + 1).padStart(2, '0');
    const anio = d.getFullYear();
    return `${dia}/${mes}/${anio}`;
}

// Formatear monto con separadores de miles
function formatearMonto(monto) {
    return parseFloat(monto).toLocaleString('es-MX', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Obtener badge de estatus
function getEstatusBadge(estatus) {
    const badges = {
        'Borrador': '<span class="badge bg-secondary">Borrador</span>',
        'Enviada': '<span class="badge bg-warning text-dark">Enviada</span>',
        'Aceptada': '<span class="badge bg-success">Aceptada</span>',
        'Cancelada': '<span class="badge bg-danger">Cancelada</span>'
    };
    return badges[estatus] || '<span class="badge bg-secondary">-</span>';
}

// Mostrar notificación
function mostrarNotificacion(mensaje, tipo = 'success') {
    const iconos = {
        'success': 'check-circle',
        'error': 'x-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    
    const colores = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    };
    
    const alert = $(`
        <div class="alert alert-${colores[tipo]} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3" 
             role="alert" style="z-index: 9999; min-width: 300px;">
            <i class="bi bi-${iconos[tipo]}"></i> ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    $('body').append(alert);
    
    setTimeout(() => {
        alert.alert('close');
    }, 5000);
}

// Confirmar acción
function confirmarAccion(mensaje, callback) {
    if (confirm(mensaje)) {
        callback();
    }
}

// Validar email
function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

// Validar número
function validarNumero(valor) {
    return !isNaN(parseFloat(valor)) && isFinite(valor);
}

// Obtener fecha actual en formato YYYY-MM-DD
function obtenerFechaActual() {
    const hoy = new Date();
    const dia = String(hoy.getDate()).padStart(2, '0');
    const mes = String(hoy.getMonth() + 1).padStart(2, '0');
    const anio = hoy.getFullYear();
    return `${anio}-${mes}-${dia}`;
}

// Parsear monto (eliminar símbolos de moneda y comas)
function parsearMonto(valor) {
    if (typeof valor === 'string') {
        valor = valor.replace(/[$,]/g, '');
    }
    return parseFloat(valor) || 0;
}

// Formatear a moneda con símbolo
function formatearMoneda(valor) {
    return '$' + formatearMonto(valor);
}

// Manejo de errores de API
function manejarErrorAPI(error) {
    console.error('Error API:', error);
    let mensaje = 'Ocurrió un error al procesar la solicitud';
    
    if (error.responseJSON && error.responseJSON.error) {
        mensaje = error.responseJSON.error;
    } else if (error.statusText) {
        mensaje = error.statusText;
    }
    
    mostrarNotificacion(mensaje, 'error');
}

// Deshabilitar botón durante operación
function deshabilitarBoton(boton, texto = 'Procesando...') {
    const $btn = $(boton);
    $btn.data('texto-original', $btn.html());
    $btn.prop('disabled', true);
    $btn.html(`<span class="spinner-border spinner-border-sm me-2"></span>${texto}`);
}

// Habilitar botón después de operación
function habilitarBoton(boton) {
    const $btn = $(boton);
    $btn.prop('disabled', false);
    $btn.html($btn.data('texto-original'));
}

// Scroll suave al inicio
function scrollAlInicio() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Cargar clientes para select
function cargarClientesSelect(elementId, valorSeleccionado = null) {
    $.get('/api/clientes', function(data) {
        const select = $(`#${elementId}`);
        select.empty();
        select.append('<option value="">Seleccionar cliente...</option>');
        
        data.clientes.forEach(function(cliente) {
            const selected = valorSeleccionado && cliente.id == valorSeleccionado ? 'selected' : '';
            select.append(`<option value="${cliente.id}" ${selected}>${cliente.nombre}</option>`);
        });
    });
}

// Event listener para cambios en select de cliente
$(document).on('change', '#cliente-id', function() {
    const clienteId = $(this).val();
    if (clienteId) {
        $.get(`/api/clientes/${clienteId}`, function(data) {
            if (data.cliente) {
                $('#cliente-telefono').val(data.cliente.telefono || '');
                $('#cliente-email').val(data.cliente.email || '');
            }
        });
    } else {
        $('#cliente-telefono').val('');
        $('#cliente-email').val('');
    }
});

// Prevenir submit accidental de formularios
$(document).on('keypress', 'input', function(e) {
    if (e.which === 13) { // Enter key
        e.preventDefault();
        return false;
    }
});

// Inicialización global
$(document).ready(function() {
    // Configurar AJAX para manejar errores globalmente
    $(document).ajaxError(function(event, jqXHR, settings, thrownError) {
        if (jqXHR.status === 404) {
            mostrarNotificacion('Recurso no encontrado', 'error');
        } else if (jqXHR.status === 500) {
            mostrarNotificacion('Error interno del servidor', 'error');
        }
    });
    
    // Tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
