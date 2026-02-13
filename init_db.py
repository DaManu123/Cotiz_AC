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
        empresa.nombre = "Cotiz AC - Servicios de Climatización"
        empresa.direccion = "Av. Principal #123, Col. Centro, Ciudad"
        empresa.telefono = "(555) 123-4567"
        empresa.email = "contacto@cotizac.com"
        empresa.redes_sociales = "Facebook: @CotizAC | Instagram: @cotizac_oficial"
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
        cotizacion.notas = "Incluye instalación y garantía de 1 año. Tiempo de entrega: 3-5 días hábiles."
        
        # Agregar detalles
        detalle1 = DetalleCotizacion()
        detalle1.cantidad = 2
        detalle1.descripcion = "Aire Acondicionado Split 12,000 BTU Inverter - Marca Premium"
        detalle1.precio_unitario = 8500.00
        detalle1.total_linea = 17000.00
        detalle1.orden = 0
        
        detalle2 = DetalleCotizacion()
        detalle2.cantidad = 2
        detalle2.descripcion = "Instalación completa de equipo incluye: tubería, cableado, soportes y mano de obra"
        detalle2.precio_unitario = 2500.00
        detalle2.total_linea = 5000.00
        detalle2.orden = 1
        
        detalle3 = DetalleCotizacion()
        detalle3.cantidad = 1
        detalle3.descripcion = "Mantenimiento preventivo (cortesía por compra)"
        detalle3.precio_unitario = 0.00
        detalle3.total_linea = 0.00
        detalle3.orden = 2
        
        detalles = [detalle1, detalle2, detalle3]
        
        for detalle in detalles:
            cotizacion.detalles.append(detalle)
        
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
