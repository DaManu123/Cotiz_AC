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
        empresa = Empresa(
            nombre="Cotiz AC - Servicios de Climatización",
            direccion="Av. Principal #123, Col. Centro, Ciudad",
            telefono="(555) 123-4567",
            email="contacto@cotizac.com",
            redes_sociales="Facebook: @CotizAC | Instagram: @cotizac_oficial"
        )
        db.session.add(empresa)
        
        # Crear clientes de ejemplo
        clientes = [
            Cliente(
                nombre="Juan Pérez González",
                telefono="555-1111",
                email="juan.perez@email.com",
                direccion="Calle Reforma 456, Col. Juárez"
            ),
            Cliente(
                nombre="María López Hernández",
                telefono="555-2222",
                email="maria.lopez@email.com",
                direccion="Av. Insurgentes 789, Col. Roma"
            ),
            Cliente(
                nombre="Empresa Construcciones XYZ S.A.",
                telefono="555-3333",
                email="contacto@construccionesxyz.com",
                direccion="Boulevard Industrial 321, Parque Industrial"
            )
        ]
        
        for cliente in clientes:
            db.session.add(cliente)
        
        db.session.commit()
        
        # Crear cotización de ejemplo
        cotizacion = Cotizacion(
            numero_cotizacion="COT-00001",
            fecha=date.today(),
            cliente_id=1,
            estatus="Enviada",
            notas="Incluye instalación y garantía de 1 año. Tiempo de entrega: 3-5 días hábiles."
        )
        
        # Agregar detalles
        detalles = [
            DetalleCotizacion(
                cantidad=2,
                descripcion="Aire Acondicionado Split 12,000 BTU Inverter - Marca Premium",
                precio_unitario=8500.00,
                total_linea=17000.00,
                orden=0
            ),
            DetalleCotizacion(
                cantidad=2,
                descripcion="Instalación completa de equipo incluye: tubería, cableado, soportes y mano de obra",
                precio_unitario=2500.00,
                total_linea=5000.00,
                orden=1
            ),
            DetalleCotizacion(
                cantidad=1,
                descripcion="Mantenimiento preventivo (cortesía por compra)",
                precio_unitario=0.00,
                total_linea=0.00,
                orden=2
            )
        ]
        
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
