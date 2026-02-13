from datetime import datetime
from src.models.models import db, Empresa


class EmpresaController:
    """Controlador para operaciones de empresa"""
    
    @staticmethod
    def obtener_empresa():
        """Obtiene los datos de la empresa (siempre hay solo uno)"""
        empresa = Empresa.query.first()
        if not empresa:
            return {'error': 'No hay datos de empresa configurados'}, 404
        return {'empresa': empresa.to_dict()}, 200
    
    @staticmethod
    def crear_o_actualizar_empresa(data):
        """Crea o actualiza los datos de la empresa"""
        try:
            empresa = Empresa.query.first()
            
            if not empresa:
                # Crear nueva empresa
                empresa = Empresa(
                    nombre=data.get('nombre', ''),
                    direccion=data.get('direccion', ''),
                    telefono=data.get('telefono', ''),
                    email=data.get('email', ''),
                    redes_sociales=data.get('redes_sociales', ''),
                    logo=data.get('logo', '')
                )
                db.session.add(empresa)
            else:
                # Actualizar empresa existente
                if 'nombre' in data:
                    empresa.nombre = data['nombre']
                if 'direccion' in data:
                    empresa.direccion = data['direccion']
                if 'telefono' in data:
                    empresa.telefono = data['telefono']
                if 'email' in data:
                    empresa.email = data['email']
                if 'redes_sociales' in data:
                    empresa.redes_sociales = data['redes_sociales']
                if 'logo' in data:
                    empresa.logo = data['logo']
                empresa.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {'success': True, 'empresa': empresa.to_dict()}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
