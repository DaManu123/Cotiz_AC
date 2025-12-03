import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'cotizaciones.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de la empresa
    EMPRESA_NOMBRE = "Aire Acondicionado Profesional"
    EMPRESA_RFC = "AAP123456789"
    EMPRESA_DIRECCION = "Calle Principal #123, Ciudad, Estado, CP 12345"
    EMPRESA_TELEFONO = "+52 (55) 1234-5678"
    EMPRESA_EMAIL = "contacto@aireacpro.com"
    
    # Configuración de impuestos
    IVA_PORCENTAJE = 16.0
    
    # Moneda
    MONEDA = "MXN"
    MONEDA_SIMBOLO = "$"
    
    # Términos y condiciones por defecto
    TERMINOS_CONDICIONES = """
TÉRMINOS Y CONDICIONES:

1. VALIDEZ: Esta cotización tiene una validez de 30 días naturales a partir de su fecha de emisión.

2. FORMA DE PAGO: 50% anticipo al confirmar el pedido, 50% restante contra entrega e instalación.

3. GARANTÍA: Los equipos cuentan con garantía del fabricante. La instalación tiene garantía de 1 año contra defectos de mano de obra.

4. TIEMPO DE ENTREGA: 5 a 10 días hábiles después de confirmado el pedido y recibido el anticipo.

5. INSTALACIÓN: Incluye mano de obra, tubería de cobre, cable eléctrico, soporte y materiales menores. No incluye obra civil o modificaciones eléctricas mayores.

6. EXCLUSIONES: No incluye trabajos de herrería, albañilería, pintura o modificaciones estructurales adicionales.

7. RESPONSABILIDAD: La empresa no se hace responsable por daños causados por mal uso, instalación no autorizada o fenómenos naturales.

8. CANCELACIONES: Las cancelaciones después de iniciar trabajos tendrán un cargo del 30% del valor total.
"""
