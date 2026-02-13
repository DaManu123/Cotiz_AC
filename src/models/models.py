from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, relationship

db = SQLAlchemy()

if TYPE_CHECKING:
    from sqlalchemy.orm import WriteOnlyMapped


class Empresa(db.Model):
    """Modelo para datos de la empresa"""
    __tablename__ = 'empresa'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    direccion = db.Column(db.String(300))
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(100))
    redes_sociales = db.Column(db.Text)  # JSON string
    logo = db.Column(db.String(200))  # Ruta al logo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'redes_sociales': self.redes_sociales,
            'logo': self.logo
        }


class Cliente(db.Model):
    """Modelo para clientes"""
    __tablename__ = 'cliente'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con cotizaciones
    cotizaciones: Mapped[List["Cotizacion"]] = relationship('Cotizacion', back_populates='cliente', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion
        }


class Cotizacion(db.Model):
    """Modelo para cotizaciones"""
    __tablename__ = 'cotizacion'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_cotizacion = db.Column(db.String(50), unique=True, nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    subtotal = db.Column(db.Float, default=0.0)
    impuestos = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)
    estatus = db.Column(db.String(50), default='Borrador')  # Borrador, Enviada, Aceptada, Cancelada
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    cliente: Mapped["Cliente"] = relationship('Cliente', back_populates='cotizaciones')
    detalles: Mapped[List["DetalleCotizacion"]] = relationship(
        'DetalleCotizacion', 
        back_populates='cotizacion', 
        lazy=True, 
        cascade='all, delete-orphan'
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_cotizacion': self.numero_cotizacion,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'cliente_id': self.cliente_id,
            'cliente': self.cliente.to_dict() if self.cliente else None,
            'subtotal': self.subtotal,
            'impuestos': self.impuestos,
            'total': self.total,
            'estatus': self.estatus,
            'notas': self.notas,
            'detalles': [d.to_dict() for d in self.detalles] if self.detalles else []
        }
    
    def calcular_totales(self):
        """Calcula subtotal, impuestos y total"""
        if self.detalles:
            self.subtotal = sum(detalle.total_linea for detalle in self.detalles)
        else:
            self.subtotal = 0.0
        # Impuestos configurables (por ahora 16%)
        self.impuestos = self.subtotal * 0.16
        self.total = self.subtotal + self.impuestos
        

class DetalleCotizacion(db.Model):
    """Modelo para detalles de cotización"""
    __tablename__ = 'detalle_cotizacion'
    
    id = db.Column(db.Integer, primary_key=True)
    cotizacion_id = db.Column(db.Integer, db.ForeignKey('cotizacion.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    total_linea = db.Column(db.Float, nullable=False)
    orden = db.Column(db.Integer, default=0)  # Para mantener el orden
    
    # Relación
    cotizacion: Mapped["Cotizacion"] = relationship('Cotizacion', back_populates='detalles')
    
    def to_dict(self):
        return {
            'id': self.id,
            'cotizacion_id': self.cotizacion_id,
            'cantidad': self.cantidad,
            'descripcion': self.descripcion,
            'precio_unitario': self.precio_unitario,
            'total_linea': self.total_linea,
            'orden': self.orden
        }
    
    def calcular_total(self):
        """Calcula el total de la línea"""
        self.total_linea = self.cantidad * self.precio_unitario
