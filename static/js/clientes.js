// JavaScript para Gestión de Clientes

let clienteEditandoId = null;

$(document).ready(function() {
    cargarClientes();
    
    // Búsqueda en tiempo real
    $('#buscar-cliente').on('input', function() {
        const busqueda = $(this).val();
        cargarClientes(busqueda);
    });
});

function cargarClientes(busqueda = '') {
    const params = busqueda ? { busqueda: busqueda } : {};
    
    $.get('/api/clientes', params, function(data) {
        const tbody = $('#tabla-clientes tbody');
        tbody.empty();
        
        $('#total-clientes').text(`${data.total} clientes`);
        
        if (data.clientes.length === 0) {
            tbody.append(`
                <tr>
                    <td colspan="6" class="text-center text-muted">
                        No hay clientes registrados
                    </td>
                </tr>
            `);
            return;
        }
        
        data.clientes.forEach(function(cliente) {
            tbody.append(`
                <tr>
                    <td>${cliente.id}</td>
                    <td><strong>${cliente.nombre}</strong></td>
                    <td>${cliente.telefono || '-'}</td>
                    <td>${cliente.email || '-'}</td>
                    <td>${cliente.direccion || '-'}</td>
                    <td>
                        <div class="btn-group btn-group-sm" role="group">
                            <button class="btn btn-outline-primary" onclick="editarCliente(${cliente.id})" title="Editar">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="eliminarCliente(${cliente.id})" title="Eliminar">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `);
        });
    });
}

function limpiarFormulario() {
    clienteEditandoId = null;
    $('#cliente-id-edit').val('');
    $('#form-cliente')[0].reset();
    $('#modal-titulo').html('<i class="bi bi-person-plus"></i> Nuevo Cliente');
}

function guardarCliente() {
    const nombre = $('#cliente-nombre').val().trim();
    
    if (!nombre) {
        mostrarNotificacion('El nombre es requerido', 'warning');
        return;
    }
    
    const data = {
        nombre: nombre,
        telefono: $('#cliente-telefono').val(),
        email: $('#cliente-email').val(),
        direccion: $('#cliente-direccion').val()
    };
    
    const metodo = clienteEditandoId ? 'PUT' : 'POST';
    const url = clienteEditandoId ? `/api/clientes/${clienteEditandoId}` : '/api/clientes';
    
    $.ajax({
        url: url,
        method: metodo,
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            const mensaje = clienteEditandoId ? 'Cliente actualizado' : 'Cliente creado';
            mostrarNotificacion(mensaje + ' exitosamente', 'success');
            
            $('#modalCliente').modal('hide');
            cargarClientes();
            limpiarFormulario();
        },
        error: function(error) {
            manejarErrorAPI(error);
        }
    });
}

function editarCliente(clienteId) {
    $.get(`/api/clientes/${clienteId}`, function(data) {
        const cliente = data.cliente;
        
        clienteEditandoId = clienteId;
        $('#cliente-id-edit').val(clienteId);
        $('#cliente-nombre').val(cliente.nombre);
        $('#cliente-telefono').val(cliente.telefono || '');
        $('#cliente-email').val(cliente.email || '');
        $('#cliente-direccion').val(cliente.direccion || '');
        
        $('#modal-titulo').html('<i class="bi bi-pencil"></i> Editar Cliente');
        $('#modalCliente').modal('show');
    });
}

function eliminarCliente(clienteId) {
    confirmarAccion('¿Está seguro de eliminar este cliente?\nEsta acción no se puede deshacer.', function() {
        $.ajax({
            url: `/api/clientes/${clienteId}`,
            method: 'DELETE',
            success: function() {
                mostrarNotificacion('Cliente eliminado exitosamente', 'success');
                cargarClientes();
            },
            error: function(error) {
                manejarErrorAPI(error);
            }
        });
    });
}
