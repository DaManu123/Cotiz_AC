from datetime import datetime
from app import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    correo = db.Column(db.String(100), nullable=True)
    
    cotizaciones = db.relationship('Cotizacion', backref='cliente', lazy=True)
    
    def __repr__(self):
        return f'<Cliente {self.nombre}>'

class Cotizacion(db.Model):
    __tablename__ = 'cotizaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
    # Campos calculados
    subtotal = db.Column(db.Float, default=0.0)
    descuento_tipo = db.Column(db.String(10), default='fixed')  # 'percent' o 'fixed'
    descuento_valor = db.Column(db.Float, default=0.0)
    descuento_monto = db.Column(db.Float, default=0.0)
    iva_porcentaje = db.Column(db.Float, default=16.0)
    iva_monto = db.Column(db.Float, default=0.0)
    envio = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)
    
    # Estado de pago
    estado_pago = db.Column(db.String(20), default='Pendiente')  # Pendiente, Parcial, Pagado
    monto_pagado = db.Column(db.Float, default=0.0)
    
    # Términos y condiciones
    terms_conditions = db.Column(db.Text, nullable=True)
    
    # Auditoría
    creado_por = db.Column(db.String(100), nullable=True)
    creado_en = db.Column(db.DateTime, default=datetime.now)
    actualizado_en = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    items = db.relationship('Item', backref='cotizacion', lazy=True, cascade='all, delete-orphan')
    
    def calcular_saldo(self):
        return round(self.total - self.monto_pagado, 2)
    
    def __repr__(self):
        return f'<Cotizacion {self.id}>'

class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    cotizacion_id = db.Column(db.Integer, db.ForeignKey('cotizaciones.id'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    unidad = db.Column(db.String(20), default='pza')
    cantidad = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    total_item = db.Column(db.Float, default=0.0)
    
    def calcular_total(self):
        self.total_item = round(self.cantidad * self.precio_unitario, 2)
        return self.total_item
    
    def __repr__(self):
        return f'<Item {self.descripcion[:30]}>'
