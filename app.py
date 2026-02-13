import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS  # type: ignore
from dotenv import load_dotenv
from src.models.models import db
from src.controllers.cotizacion_controller import CotizacionController
from src.controllers.cliente_controller import ClienteController
from src.controllers.empresa_controller import EmpresaController
from src.services.pdf_service import PDFService
from src.services.excel_service import ExcelService

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Configuración
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cotizaciones.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar base de datos
db.init_app(app)

# Servicios
pdf_service = PDFService()
excel_service = ExcelService()


# ==================== RUTAS PRINCIPALES ====================

@app.route('/')
def index():
    """Página principal - Dashboard"""
    return render_template('index.html')


@app.route('/nueva-cotizacion')
def nueva_cotizacion():
    """Página para crear nueva cotización"""
    return render_template('nueva_cotizacion.html')


@app.route('/historial')
def historial():
    """Página de historial de cotizaciones"""
    return render_template('historial.html')


@app.route('/clientes')
def clientes():
    """Página de gestión de clientes"""
    return render_template('clientes.html')


@app.route('/configuracion')
def configuracion():
    """Página de configuración de empresa"""
    return render_template('configuracion.html')


# ==================== API COTIZACIONES ====================

@app.route('/api/cotizaciones', methods=['GET'])
def api_obtener_cotizaciones():
    """Obtiene todas las cotizaciones con filtros opcionales"""
    filtros = {}
    if request.args.get('cliente_id'):
        filtros['cliente_id'] = request.args.get('cliente_id')
    if request.args.get('estatus'):
        filtros['estatus'] = request.args.get('estatus')
    if request.args.get('fecha_desde'):
        filtros['fecha_desde'] = request.args.get('fecha_desde')
    if request.args.get('fecha_hasta'):
        filtros['fecha_hasta'] = request.args.get('fecha_hasta')
    
    result, status = CotizacionController.obtener_todas(filtros)
    return jsonify(result), status


@app.route('/api/cotizaciones/<int:cotizacion_id>', methods=['GET'])
def api_obtener_cotizacion(cotizacion_id):
    """Obtiene una cotización específica"""
    result, status = CotizacionController.obtener_cotizacion(cotizacion_id)
    return jsonify(result), status


@app.route('/api/cotizaciones', methods=['POST'])
def api_crear_cotizacion():
    """Crea una nueva cotización"""
    data = request.get_json()
    result, status = CotizacionController.crear_cotizacion(data)
    return jsonify(result), status


@app.route('/api/cotizaciones/<int:cotizacion_id>', methods=['PUT'])
def api_actualizar_cotizacion(cotizacion_id):
    """Actualiza una cotización existente"""
    data = request.get_json()
    result, status = CotizacionController.actualizar_cotizacion(cotizacion_id, data)
    return jsonify(result), status


@app.route('/api/cotizaciones/<int:cotizacion_id>', methods=['DELETE'])
def api_eliminar_cotizacion(cotizacion_id):
    """Elimina una cotización"""
    result, status = CotizacionController.eliminar_cotizacion(cotizacion_id)
    return jsonify(result), status


@app.route('/api/cotizaciones/<int:cotizacion_id>/estatus', methods=['PATCH'])
def api_cambiar_estatus(cotizacion_id):
    """Cambia el estatus de una cotización"""
    data = request.get_json()
    nuevo_estatus = data.get('estatus')
    result, status = CotizacionController.cambiar_estatus(cotizacion_id, nuevo_estatus)
    return jsonify(result), status


@app.route('/api/cotizaciones/consecutivo', methods=['GET'])
def api_obtener_consecutivo():
    """Obtiene el siguiente número consecutivo"""
    consecutivo = CotizacionController.generar_consecutivo()
    return jsonify({'numero_cotizacion': consecutivo}), 200


# ==================== API CLIENTES ====================

@app.route('/api/clientes', methods=['GET'])
def api_obtener_clientes():
    """Obtiene todos los clientes"""
    busqueda = request.args.get('busqueda')
    result, status = ClienteController.obtener_todos(busqueda)
    return jsonify(result), status


@app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
def api_obtener_cliente(cliente_id):
    """Obtiene un cliente específico"""
    result, status = ClienteController.obtener_cliente(cliente_id)
    return jsonify(result), status


@app.route('/api/clientes', methods=['POST'])
def api_crear_cliente():
    """Crea un nuevo cliente"""
    data = request.get_json()
    result, status = ClienteController.crear_cliente(data)
    return jsonify(result), status


@app.route('/api/clientes/<int:cliente_id>', methods=['PUT'])
def api_actualizar_cliente(cliente_id):
    """Actualiza un cliente existente"""
    data = request.get_json()
    result, status = ClienteController.actualizar_cliente(cliente_id, data)
    return jsonify(result), status


@app.route('/api/clientes/<int:cliente_id>', methods=['DELETE'])
def api_eliminar_cliente(cliente_id):
    """Elimina un cliente"""
    result, status = ClienteController.eliminar_cliente(cliente_id)
    return jsonify(result), status


# ==================== API EMPRESA ====================

@app.route('/api/empresa', methods=['GET'])
def api_obtener_empresa():
    """Obtiene datos de la empresa"""
    result, status = EmpresaController.obtener_empresa()
    return jsonify(result), status


@app.route('/api/empresa', methods=['POST', 'PUT'])
def api_guardar_empresa():
    """Crea o actualiza datos de la empresa"""
    data = request.get_json()
    result, status = EmpresaController.crear_o_actualizar_empresa(data)
    return jsonify(result), status


# ==================== API EXPORTACIONES ====================

@app.route('/api/cotizaciones/<int:cotizacion_id>/export/pdf', methods=['GET'])
def api_exportar_pdf(cotizacion_id):
    """Genera y descarga PDF de cotización"""
    try:
        # Obtener datos de cotización
        result, status = CotizacionController.obtener_cotizacion(cotizacion_id)
        if status != 200:
            return jsonify(result), status
        
        cotizacion_data = result['cotizacion']
        
        # Obtener datos de empresa
        empresa_result, empresa_status = EmpresaController.obtener_empresa()
        empresa_data = empresa_result.get('empresa', {}) if empresa_status == 200 else {}
        
        # Generar PDF
        filepath = pdf_service.generar_cotizacion(cotizacion_data, empresa_data)
        
        # Enviar archivo
        numero_cot = cotizacion_data['numero_cotizacion'] if isinstance(cotizacion_data, dict) else 'cotizacion'
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"{numero_cot}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/cotizaciones/<int:cotizacion_id>/export/excel', methods=['GET'])
def api_exportar_excel(cotizacion_id):
    """Genera y descarga Excel de cotización"""
    try:
        # Obtener datos de cotización
        result, status = CotizacionController.obtener_cotizacion(cotizacion_id)
        if status != 200:
            return jsonify(result), status
        
        cotizacion_data = result['cotizacion']
        
        # Obtener datos de empresa
        empresa_result, empresa_status = EmpresaController.obtener_empresa()
        empresa_data = empresa_result.get('empresa', {}) if empresa_status == 200 else {}
        
        # Generar Excel
        filepath = excel_service.generar_cotizacion(cotizacion_data, empresa_data)  # type: ignore
        
        # Enviar archivo
        numero_cot = cotizacion_data['numero_cotizacion'] if isinstance(cotizacion_data, dict) else 'cotizacion'
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"{numero_cot}.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Error interno del servidor'}), 500


# ==================== EJECUCIÓN ====================

if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs('exports/pdf', exist_ok=True)
    os.makedirs('exports/excel', exist_ok=True)
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    # Ejecutar aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
