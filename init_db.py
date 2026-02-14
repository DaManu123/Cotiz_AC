"""
Script para inicializar la base de datos y crear datos de ejemplo
"""
from app import app, db
from src.models.models import Empresa, Cliente, Cotizacion, DetalleCotizacion
from datetime import datetime, date


def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        
        # Verificar si ya existen datos
        if Empresa.query.first():
            print("La base de datos ya contiene datos.")
            return
        
        print("Insertando datos de ejemplo...")
        
        # Crear empresa
        empresa = Empresa()
        empresa.nombre = "Multiservicios RMG"
        empresa.direccion = "Av. Principal #123, Col. Centro, Ciudad"
        empresa.telefono = "(555) 123-4567"
        empresa.email = "contacto@multiserviciosrmg.com"
        empresa.rfc = "MRM2501011A1"
        empresa.redes_sociales = "Facebook: @MultiserviciosRMG | Instagram: @multiservicios_rmg"
        db.session.add(empresa)
        
        # Crear clientes de ejemplo
        cliente1 = Cliente()
        cliente1.nombre = "Juan Pérez González"
        cliente1.telefono = "555-1111"
        cliente1.email = "juan.perez@email.com"
        cliente1.direccion = "Calle Reforma 456, Col. Juárez"
        
        cliente2 = Cliente()
        cliente2.nombre = "María López Hernández"
        cliente2.telefono = "555-2222"
        cliente2.email = "maria.lopez@email.com"
        cliente2.direccion = "Av. Insurgentes 789, Col. Roma"
        
        cliente3 = Cliente()
        cliente3.nombre = "Empresa Construcciones XYZ S.A."
        cliente3.telefono = "555-3333"
        cliente3.email = "contacto@construccionesxyz.com"
        cliente3.direccion = "Boulevard Industrial 321, Parque Industrial"
        
        clientes = [cliente1, cliente2, cliente3]
        
        for cliente in clientes:
            db.session.add(cliente)
        
        db.session.commit()
        
        # Crear cotización de ejemplo
        cotizacion = Cotizacion()
        cotizacion.numero_cotizacion = "COT-00001"
        cotizacion.fecha = date.today()
        cotizacion.cliente_id = 1
        cotizacion.estatus = "Enviada"
        cotizacion.descuento = 0
        cotizacion.envio_delivery = 0
        cotizacion.notas = "1.- Cotización válida por 30 días\n2.- Precio con IVA\n3.- Entregando el producto o ejecutado el servicio no existen devoluciones."
        
        # Agregar detalles con grupos/ciudades
        detalles_data = [
            # Hermosillo
            ("Hermosillo", 11, "Bases de Herrería", 646.55),
            ("Hermosillo", 3, "Modificaciones", 258.62),
            ("Hermosillo", 52, "Cableado 3x12 (M)", 59.48),
            ("Hermosillo", 45, "Cableado 3x12 (M)", 59.48),
            ("Hermosillo", 2, "Térmico 2x30", 344.83),
            # Navojoa
            ("Navojoa", 78, "Cableado 3x12 (M)", 59.48),
            ("Navojoa", 72, "Tubería flexible metálica 1/2 (M)", 30.17),
            ("Navojoa", 1, "Térmico 2x30", 344.83),
            # Cajeme
            ("Cajeme", 55, "Cableado 3x12 (M)", 59.48),
            ("Cajeme", 1, "Bases de Herrería", 646.55),
        ]
        
        for idx, (grupo, cant, desc, pu) in enumerate(detalles_data):
            det = DetalleCotizacion()
            det.grupo = grupo
            det.cantidad = cant
            det.descripcion = desc
            det.precio_unitario = pu
            det.total_linea = cant * pu
            det.orden = idx
            cotizacion.detalles.append(det)
        
        cotizacion.calcular_totales()
        db.session.add(cotizacion)
        db.session.commit()
        
        print("✅ Base de datos inicializada correctamente!")
        print(f"✅ Empresa creada: {empresa.nombre}")
        print(f"✅ {len(clientes)} clientes creados")
        print(f"✅ 1 cotización de ejemplo creada: {cotizacion.numero_cotizacion}")
        print(f"\n💡 Puedes acceder al sistema en: http://localhost:5000")


if __name__ == '__main__':
    init_database()
