from datetime import datetime
from src.models.models import db, Cotizacion, DetalleCotizacion


class CotizacionController:
    """Controlador para operaciones de cotizaciones"""
    
    @staticmethod
    def generar_consecutivo():
        """Genera el siguiente número consecutivo de cotización"""
        ultima_cotizacion = Cotizacion.query.order_by(Cotizacion.id.desc()).first()
        
        if ultima_cotizacion:
            # Extraer número del formato COT-00001
            ultimo_numero = int(ultima_cotizacion.numero_cotizacion.split('-')[1])
            nuevo_numero = ultimo_numero + 1
        else:
            nuevo_numero = 1
        
        return f"COT-{nuevo_numero:05d}"
    
    @staticmethod
    def crear_cotizacion(data):
        """
        Crea una nueva cotización
        
        Args:
            data: dict con estructura:
                {
                    'cliente_id': int,
                    'fecha': str (YYYY-MM-DD),
                    'notas': str,
                    'detalles': [
                        {
                            'cantidad': float,
                            'descripcion': str,
                            'precio_unitario': float
                        }
                    ]
                }
        """
        try:
            # Validar cliente
            if not data.get('cliente_id'):
                return {'error': 'Cliente es requerido'}, 400
            
            # Generar número consecutivo
            numero_cotizacion = CotizacionController.generar_consecutivo()
            
            # Crear cotización
            cotizacion = Cotizacion()
            cotizacion.numero_cotizacion = numero_cotizacion
            cotizacion.fecha = datetime.strptime(data.get('fecha', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
            cotizacion.cliente_id = data['cliente_id']
            cotizacion.notas = data.get('notas', '')
            cotizacion.descuento = data.get('descuento', 0) or 0
            cotizacion.envio_delivery = data.get('envio_delivery', 0) or 0
            cotizacion.estatus = 'Borrador'
            
            # Agregar detalles
            if data.get('detalles'):
                for idx, detalle_data in enumerate(data['detalles']):
                    detalle = DetalleCotizacion()
                    detalle.grupo = detalle_data.get('grupo', '')
                    detalle.cantidad = detalle_data['cantidad']
                    detalle.descripcion = detalle_data['descripcion']
                    detalle.precio_unitario = detalle_data['precio_unitario']
                    detalle.orden = idx
                    detalle.calcular_total()
                    cotizacion.detalles.append(detalle)
            
            # Calcular totales
            cotizacion.calcular_totales()
            
            # Guardar en base de datos
            db.session.add(cotizacion)
            db.session.commit()
            
            return {'success': True, 'cotizacion': cotizacion.to_dict()}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    @staticmethod
    def obtener_cotizacion(cotizacion_id):
        """Obtiene una cotización por ID"""
        cotizacion = Cotizacion.query.get(cotizacion_id)
        if not cotizacion:
            return {'error': 'Cotización no encontrada'}, 404
        return {'cotizacion': cotizacion.to_dict()}, 200
    
    @staticmethod
    def obtener_todas(filtros=None):
        """
        Obtiene todas las cotizaciones con filtros opcionales
        
        Args:
            filtros: dict con cliente_id, estatus, fecha_desde, fecha_hasta
        """
        query = Cotizacion.query
        
        if filtros:
            if filtros.get('cliente_id'):
                query = query.filter_by(cliente_id=filtros['cliente_id'])
            if filtros.get('estatus'):
                query = query.filter_by(estatus=filtros['estatus'])
            if filtros.get('fecha_desde'):
                query = query.filter(Cotizacion.fecha >= filtros['fecha_desde'])
            if filtros.get('fecha_hasta'):
                query = query.filter(Cotizacion.fecha <= filtros['fecha_hasta'])
        
        cotizaciones = query.order_by(Cotizacion.fecha.desc()).all()
        return {
            'cotizaciones': [c.to_dict() for c in cotizaciones],
            'total': len(cotizaciones)
        }, 200
    
    @staticmethod
    def actualizar_cotizacion(cotizacion_id, data):
        """Actualiza una cotización existente"""
        try:
            cotizacion = Cotizacion.query.get(cotizacion_id)
            if not cotizacion:
                return {'error': 'Cotización no encontrada'}, 404
            
            # Actualizar campos básicos
            if 'cliente_id' in data:
                cotizacion.cliente_id = data['cliente_id']
            if 'fecha' in data:
                cotizacion.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d')
            if 'notas' in data:
                cotizacion.notas = data['notas']
            if 'descuento' in data:
                cotizacion.descuento = data['descuento'] or 0
            if 'envio_delivery' in data:
                cotizacion.envio_delivery = data['envio_delivery'] or 0
            if 'estatus' in data:
                cotizacion.estatus = data['estatus']
            
            # Actualizar detalles si se proporcionan
            if 'detalles' in data:
                # Eliminar detalles existentes
                DetalleCotizacion.query.filter_by(cotizacion_id=cotizacion_id).delete()
                
                # Agregar nuevos detalles
                for idx, detalle_data in enumerate(data['detalles']):
                    detalle = DetalleCotizacion()
                    detalle.cotizacion_id = cotizacion_id
                    detalle.grupo = detalle_data.get('grupo', '')
                    detalle.cantidad = detalle_data['cantidad']
                    detalle.descripcion = detalle_data['descripcion']
                    detalle.precio_unitario = detalle_data['precio_unitario']
                    detalle.orden = idx
                    detalle.calcular_total()
                    db.session.add(detalle)
                
                # Recalcular totales
                db.session.flush()
                cotizacion.calcular_totales()
            
            cotizacion.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {'success': True, 'cotizacion': cotizacion.to_dict()}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    @staticmethod
    def eliminar_cotizacion(cotizacion_id):
        """Elimina una cotización"""
        try:
            cotizacion = Cotizacion.query.get(cotizacion_id)
            if not cotizacion:
                return {'error': 'Cotización no encontrada'}, 404
            
            db.session.delete(cotizacion)
            db.session.commit()
            
            return {'success': True, 'message': 'Cotización eliminada'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    @staticmethod
    def cambiar_estatus(cotizacion_id, nuevo_estatus):
        """Cambia el estatus de una cotización"""
        try:
            cotizacion = Cotizacion.query.get(cotizacion_id)
            if not cotizacion:
                return {'error': 'Cotización no encontrada'}, 404
            
            estatus_validos = ['Borrador', 'Enviada', 'Aceptada', 'Cancelada']
            if nuevo_estatus not in estatus_validos:
                return {'error': f'Estatus inválido. Valores permitidos: {estatus_validos}'}, 400
            
            cotizacion.estatus = nuevo_estatus
            cotizacion.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {'success': True, 'cotizacion': cotizacion.to_dict()}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
