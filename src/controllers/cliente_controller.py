from src.models.models import db, Cliente


class ClienteController:
    """Controlador para operaciones de clientes"""
    
    @staticmethod
    def crear_cliente(data):
        """
        Crea un nuevo cliente
        
        Args:
            data: dict con nombre, telefono, email, direccion
        """
        try:
            if not data.get('nombre'):
                return {'error': 'Nombre es requerido'}, 400
            
            cliente = Cliente(
                nombre=data['nombre'],
                telefono=data.get('telefono', ''),
                email=data.get('email', ''),
                direccion=data.get('direccion', '')
            )
            
            db.session.add(cliente)
            db.session.commit()
            
            return {'success': True, 'cliente': cliente.to_dict()}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    @staticmethod
    def obtener_cliente(cliente_id):
        """Obtiene un cliente por ID"""
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return {'error': 'Cliente no encontrado'}, 404
        return {'cliente': cliente.to_dict()}, 200
    
    @staticmethod
    def obtener_todos(busqueda=None):
        """
        Obtiene todos los clientes con búsqueda opcional
        
        Args:
            busqueda: str para filtrar por nombre
        """
        query = Cliente.query
        
        if busqueda:
            query = query.filter(Cliente.nombre.ilike(f'%{busqueda}%'))
        
        clientes = query.order_by(Cliente.nombre).all()
        return {
            'clientes': [c.to_dict() for c in clientes],
            'total': len(clientes)
        }, 200
    
    @staticmethod
    def actualizar_cliente(cliente_id, data):
        """Actualiza un cliente existente"""
        try:
            cliente = Cliente.query.get(cliente_id)
            if not cliente:
                return {'error': 'Cliente no encontrado'}, 404
            
            if 'nombre' in data:
                cliente.nombre = data['nombre']
            if 'telefono' in data:
                cliente.telefono = data['telefono']
            if 'email' in data:
                cliente.email = data['email']
            if 'direccion' in data:
                cliente.direccion = data['direccion']
            
            db.session.commit()
            
            return {'success': True, 'cliente': cliente.to_dict()}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    @staticmethod
    def eliminar_cliente(cliente_id):
        """Elimina un cliente"""
        try:
            cliente = Cliente.query.get(cliente_id)
            if not cliente:
                return {'error': 'Cliente no encontrado'}, 404
            
            # Verificar si tiene cotizaciones asociadas
            if cliente.cotizaciones:
                return {
                    'error': 'No se puede eliminar el cliente porque tiene cotizaciones asociadas'
                }, 400
            
            db.session.delete(cliente)
            db.session.commit()
            
            return {'success': True, 'message': 'Cliente eliminado'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
