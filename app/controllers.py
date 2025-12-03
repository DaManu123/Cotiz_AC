import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Cliente, Cotizacion, Item
from app.utils import calcular_totales, exportar_excel, generar_pdf

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Lista de cotizaciones con filtros opcionales."""
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    cliente_nombre = request.args.get('cliente')
    estado = request.args.get('estado')
    
    query = Cotizacion.query
    
    if fecha_desde:
        try:
            fecha_d = datetime.strptime(fecha_desde, '%Y-%m-%d')
            query = query.filter(Cotizacion.fecha >= fecha_d)
        except ValueError:
            pass
    
    if fecha_hasta:
        try:
            fecha_h = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            query = query.filter(Cotizacion.fecha <= fecha_h)
        except ValueError:
            pass
    
    if cliente_nombre:
        query = query.join(Cliente).filter(Cliente.nombre.ilike(f'%{cliente_nombre}%'))
    
    if estado:
        query = query.filter(Cotizacion.estado_pago == estado)
    
    cotizaciones = query.order_by(Cotizacion.fecha.desc()).all()
    
    return render_template('cotizacion_list.html', cotizaciones=cotizaciones)

@bp.route('/cotizacion/nueva', methods=['GET'])
def nueva_cotizacion():
    """Formulario para nueva cotización."""
    return render_template('cotizacion_form.html', cotizacion=None)

@bp.route('/cotizacion', methods=['POST'])
def crear_cotizacion():
    """Crear nueva cotización."""
    try:
        # Datos del cliente
        cliente_nombre = request.form.get('cliente_nombre', '').strip()
        cliente_telefono = request.form.get('cliente_telefono', '').strip()
        cliente_correo = request.form.get('cliente_correo', '').strip()
        
        cliente = None
        if cliente_nombre:
            cliente = Cliente(
                nombre=cliente_nombre,
                telefono=cliente_telefono,
                correo=cliente_correo
            )
            db.session.add(cliente)
            db.session.flush()
        
        # Datos de la cotización
        fecha_str = request.form.get('fecha')
        if fecha_str:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        else:
            fecha = datetime.now()
        
        descuento_tipo = request.form.get('descuento_tipo', 'fixed')
        descuento_valor = float(request.form.get('descuento_valor', 0))
        iva_porcentaje = float(request.form.get('iva_porcentaje', current_app.config['IVA_PORCENTAJE']))
        envio = float(request.form.get('envio', 0))
        creado_por = request.form.get('creado_por', 'Usuario')
        
        # Crear cotización
        cotizacion = Cotizacion(
            cliente_id=cliente.id if cliente else None,
            fecha=fecha,
            descuento_tipo=descuento_tipo,
            descuento_valor=descuento_valor,
            iva_porcentaje=iva_porcentaje,
            envio=envio,
            creado_por=creado_por,
            terms_conditions=current_app.config['TERMINOS_CONDICIONES']
        )
        db.session.add(cotizacion)
        db.session.flush()
        
        # Procesar items
        items_data = []
        descripciones = request.form.getlist('item_descripcion[]')
        unidades = request.form.getlist('item_unidad[]')
        cantidades = request.form.getlist('item_cantidad[]')
        precios = request.form.getlist('item_precio[]')
        
        if not descripciones:
            flash('Debe agregar al menos un item', 'error')
            db.session.rollback()
            return redirect(url_for('main.nueva_cotizacion'))
        
        for i in range(len(descripciones)):
            if descripciones[i].strip():
                cantidad = float(cantidades[i])
                precio_unitario = float(precios[i])
                
                if cantidad <= 0:
                    flash(f'La cantidad del item {i+1} debe ser mayor a 0', 'error')
                    db.session.rollback()
                    return redirect(url_for('main.nueva_cotizacion'))
                
                if precio_unitario < 0:
                    flash(f'El precio del item {i+1} no puede ser negativo', 'error')
                    db.session.rollback()
                    return redirect(url_for('main.nueva_cotizacion'))
                
                item = Item(
                    cotizacion_id=cotizacion.id,
                    descripcion=descripciones[i].strip(),
                    unidad=unidades[i].strip() or 'pza',
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )
                item.calcular_total()
                db.session.add(item)
                
                items_data.append({
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario
                })
        
        # Calcular totales
        totales = calcular_totales(items_data, descuento_tipo, descuento_valor, iva_porcentaje, envio)
        
        cotizacion.subtotal = totales['subtotal']
        cotizacion.descuento_monto = totales['descuento_monto']
        cotizacion.iva_monto = totales['iva_monto']
        cotizacion.total = totales['total']
        
        db.session.commit()
        
        flash(f'Cotización #{cotizacion.id} creada exitosamente', 'success')
        return redirect(url_for('main.ver_cotizacion', id=cotizacion.id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear cotización: {str(e)}', 'error')
        return redirect(url_for('main.nueva_cotizacion'))

@bp.route('/cotizacion/<int:id>')
def ver_cotizacion(id):
    """Ver detalles de una cotización."""
    cotizacion = Cotizacion.query.get_or_404(id)
    return render_template('cotizacion_form.html', cotizacion=cotizacion, readonly=True)

@bp.route('/cotizacion/<int:id>/editar', methods=['GET'])
def editar_cotizacion(id):
    """Formulario para editar cotización."""
    cotizacion = Cotizacion.query.get_or_404(id)
    return render_template('cotizacion_form.html', cotizacion=cotizacion, readonly=False)

@bp.route('/cotizacion/<int:id>/actualizar', methods=['POST'])
def actualizar_cotizacion(id):
    """Actualizar cotización existente."""
    cotizacion = Cotizacion.query.get_or_404(id)
    
    try:
        # Actualizar cliente
        if cotizacion.cliente:
            cotizacion.cliente.nombre = request.form.get('cliente_nombre', '').strip()
            cotizacion.cliente.telefono = request.form.get('cliente_telefono', '').strip()
            cotizacion.cliente.correo = request.form.get('cliente_correo', '').strip()
        elif request.form.get('cliente_nombre', '').strip():
            cliente = Cliente(
                nombre=request.form.get('cliente_nombre', '').strip(),
                telefono=request.form.get('cliente_telefono', '').strip(),
                correo=request.form.get('cliente_correo', '').strip()
            )
            db.session.add(cliente)
            db.session.flush()
            cotizacion.cliente_id = cliente.id
        
        # Actualizar datos de cotización
        fecha_str = request.form.get('fecha')
        if fecha_str:
            cotizacion.fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        
        cotizacion.descuento_tipo = request.form.get('descuento_tipo', 'fixed')
        cotizacion.descuento_valor = float(request.form.get('descuento_valor', 0))
        cotizacion.iva_porcentaje = float(request.form.get('iva_porcentaje', current_app.config['IVA_PORCENTAJE']))
        cotizacion.envio = float(request.form.get('envio', 0))
        cotizacion.actualizado_en = datetime.now()
        
        # Eliminar items existentes
        Item.query.filter_by(cotizacion_id=cotizacion.id).delete()
        
        # Agregar nuevos items
        items_data = []
        descripciones = request.form.getlist('item_descripcion[]')
        unidades = request.form.getlist('item_unidad[]')
        cantidades = request.form.getlist('item_cantidad[]')
        precios = request.form.getlist('item_precio[]')
        
        for i in range(len(descripciones)):
            if descripciones[i].strip():
                cantidad = float(cantidades[i])
                precio_unitario = float(precios[i])
                
                if cantidad <= 0 or precio_unitario < 0:
                    flash(f'Valores inválidos en item {i+1}', 'error')
                    db.session.rollback()
                    return redirect(url_for('main.editar_cotizacion', id=id))
                
                item = Item(
                    cotizacion_id=cotizacion.id,
                    descripcion=descripciones[i].strip(),
                    unidad=unidades[i].strip() or 'pza',
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )
                item.calcular_total()
                db.session.add(item)
                
                items_data.append({
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario
                })
        
        # Recalcular totales
        totales = calcular_totales(
            items_data,
            cotizacion.descuento_tipo,
            cotizacion.descuento_valor,
            cotizacion.iva_porcentaje,
            cotizacion.envio
        )
        
        cotizacion.subtotal = totales['subtotal']
        cotizacion.descuento_monto = totales['descuento_monto']
        cotizacion.iva_monto = totales['iva_monto']
        cotizacion.total = totales['total']
        
        db.session.commit()
        
        flash(f'Cotización #{cotizacion.id} actualizada exitosamente', 'success')
        return redirect(url_for('main.ver_cotizacion', id=cotizacion.id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar cotización: {str(e)}', 'error')
        return redirect(url_for('main.editar_cotizacion', id=id))

@bp.route('/cotizacion/<int:id>/exportar/excel', methods=['POST', 'GET'])
def exportar_cotizacion_excel(id):
    """Exportar cotización a Excel."""
    cotizacion = Cotizacion.query.get_or_404(id)
    
    # Crear directorio temporal si no existe
    temp_dir = os.path.join(current_app.root_path, '..', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    filename = f'Cotizacion_{id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    filepath = os.path.join(temp_dir, filename)
    
    exportar_excel(cotizacion, filepath)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@bp.route('/cotizacion/<int:id>/exportar/pdf', methods=['GET'])
def exportar_cotizacion_pdf(id):
    """Exportar cotización a PDF."""
    cotizacion = Cotizacion.query.get_or_404(id)
    
    # Crear directorio temporal si no existe
    temp_dir = os.path.join(current_app.root_path, '..', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    filename = f'Cotizacion_{id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    filepath = os.path.join(temp_dir, filename)
    
    generar_pdf(cotizacion, filepath)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@bp.route('/cotizacion/<int:id>/pago', methods=['POST'])
def registrar_pago(id):
    """Registrar pago de una cotización."""
    cotizacion = Cotizacion.query.get_or_404(id)
    
    try:
        monto_pago = float(request.form.get('monto_pago', 0))
        
        if monto_pago < 0:
            flash('El monto del pago no puede ser negativo', 'error')
            return redirect(url_for('main.ver_cotizacion', id=id))
        
        cotizacion.monto_pagado += monto_pago
        
        if cotizacion.monto_pagado >= cotizacion.total:
            cotizacion.estado_pago = 'Pagado'
            cotizacion.monto_pagado = cotizacion.total  # Ajustar si se pagó de más
        elif cotizacion.monto_pagado > 0:
            cotizacion.estado_pago = 'Parcial'
        else:
            cotizacion.estado_pago = 'Pendiente'
        
        cotizacion.actualizado_en = datetime.now()
        db.session.commit()
        
        flash(f'Pago de ${monto_pago:,.2f} registrado. Saldo pendiente: ${cotizacion.calcular_saldo():,.2f}', 'success')
        return redirect(url_for('main.ver_cotizacion', id=id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar pago: {str(e)}', 'error')
        return redirect(url_for('main.ver_cotizacion', id=id))

@bp.route('/cotizacion/<int:id>/eliminar', methods=['POST'])
def eliminar_cotizacion(id):
    """Eliminar una cotización."""
    cotizacion = Cotizacion.query.get_or_404(id)
    
    try:
        db.session.delete(cotizacion)
        db.session.commit()
        flash(f'Cotización #{id} eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cotización: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))
