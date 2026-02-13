// JavaScript para Configuración de Empresa

$(document).ready(function() {
    cargarDatosEmpresa();
    
    $('#form-empresa').on('submit', function(e) {
        e.preventDefault();
        guardarEmpresa();
    });
});

function cargarDatosEmpresa() {
    $.get('/api/empresa', function(data) {
        if (data.empresa) {
            const empresa = data.empresa;
            $('#empresa-nombre').val(empresa.nombre || '');
            $('#empresa-direccion').val(empresa.direccion || '');
            $('#empresa-telefono').val(empresa.telefono || '');
            $('#empresa-email').val(empresa.email || '');
            $('#empresa-redes').val(empresa.redes_sociales || '');
        }
    }).fail(function(error) {
        if (error.status === 404) {
            // No hay empresa configurada, dejar campos vacíos
            console.log('No hay empresa configurada aún');
        } else {
            manejarErrorAPI(error);
        }
    });
}

function guardarEmpresa() {
    const nombre = $('#empresa-nombre').val().trim();
    
    if (!nombre) {
        mostrarNotificacion('El nombre de la empresa es requerido', 'warning');
        return;
    }
    
    const data = {
        nombre: nombre,
        direccion: $('#empresa-direccion').val(),
        telefono: $('#empresa-telefono').val(),
        email: $('#empresa-email').val(),
        redes_sociales: $('#empresa-redes').val()
    };
    
    const btnGuardar = $('button[type="submit"]');
    deshabilitarBoton(btnGuardar, 'Guardando...');
    
    $.ajax({
        url: '/api/empresa',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            habilitarBoton(btnGuardar);
            mostrarNotificacion('Configuración guardada exitosamente', 'success');
            scrollAlInicio();
        },
        error: function(error) {
            habilitarBoton(btnGuardar);
            manejarErrorAPI(error);
        }
    });
}
