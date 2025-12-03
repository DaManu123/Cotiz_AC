import pytest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils import calcular_totales

def test_calcular_totales_sin_descuento():
    """Test de cálculo sin descuento"""
    items = [
        {'cantidad': 2, 'precio_unitario': 100.0},
        {'cantidad': 1, 'precio_unitario': 50.0}
    ]
    
    resultado = calcular_totales(
        items=items,
        descuento_tipo='fixed',
        descuento_valor=0,
        iva_porcentaje=16.0,
        envio=0
    )
    
    assert resultado['subtotal'] == 250.0
    assert resultado['descuento_monto'] == 0.0
    assert resultado['base_impuesto'] == 250.0
    assert resultado['iva_monto'] == 40.0
    assert resultado['total'] == 290.0

def test_calcular_totales_con_descuento_fijo():
    """Test de cálculo con descuento en monto fijo"""
    items = [
        {'cantidad': 2, 'precio_unitario': 100.0},
        {'cantidad': 1, 'precio_unitario': 50.0}
    ]
    
    resultado = calcular_totales(
        items=items,
        descuento_tipo='fixed',
        descuento_valor=50.0,
        iva_porcentaje=16.0,
        envio=0
    )
    
    assert resultado['subtotal'] == 250.0
    assert resultado['descuento_monto'] == 50.0
    assert resultado['base_impuesto'] == 200.0
    assert resultado['iva_monto'] == 32.0
    assert resultado['total'] == 232.0

def test_calcular_totales_con_descuento_porcentaje():
    """Test de cálculo con descuento en porcentaje"""
    items = [
        {'cantidad': 2, 'precio_unitario': 100.0},
        {'cantidad': 1, 'precio_unitario': 50.0}
    ]
    
    resultado = calcular_totales(
        items=items,
        descuento_tipo='percent',
        descuento_valor=10.0,  # 10%
        iva_porcentaje=16.0,
        envio=0
    )
    
    assert resultado['subtotal'] == 250.0
    assert resultado['descuento_monto'] == 25.0  # 10% de 250
    assert resultado['base_impuesto'] == 225.0
    assert resultado['iva_monto'] == 36.0
    assert resultado['total'] == 261.0

def test_calcular_totales_con_envio():
    """Test de cálculo con envío incluido"""
    items = [
        {'cantidad': 1, 'precio_unitario': 1000.0}
    ]
    
    resultado = calcular_totales(
        items=items,
        descuento_tipo='fixed',
        descuento_valor=0,
        iva_porcentaje=16.0,
        envio=150.0
    )
    
    assert resultado['subtotal'] == 1000.0
    assert resultado['descuento_monto'] == 0.0
    assert resultado['base_impuesto'] == 1000.0
    assert resultado['iva_monto'] == 160.0
    assert resultado['total'] == 1310.0

def test_calcular_totales_cantidades_decimales():
    """Test de cálculo con cantidades decimales"""
    items = [
        {'cantidad': 2.5, 'precio_unitario': 123.45},
        {'cantidad': 1.75, 'precio_unitario': 89.99}
    ]
    
    resultado = calcular_totales(
        items=items,
        descuento_tipo='percent',
        descuento_valor=5.0,  # 5%
        iva_porcentaje=16.0,
        envio=50.0
    )
    
    # Subtotal: (2.5 * 123.45) + (1.75 * 89.99) = 308.625 + 157.4825 = 466.11
    assert resultado['subtotal'] == 466.11
    # Descuento: 466.11 * 0.05 = 23.31
    assert resultado['descuento_monto'] == 23.31
    # Base: 466.11 - 23.31 = 442.80
    assert resultado['base_impuesto'] == 442.80
    # IVA: 442.80 * 0.16 = 70.85
    assert resultado['iva_monto'] == 70.85
    # Total: 442.80 + 70.85 + 50 = 563.65
    assert resultado['total'] == 563.65

def test_calcular_totales_caso_completo():
    """Test de cálculo con todos los elementos"""
    items = [
        {'cantidad': 3, 'precio_unitario': 5000.0},
        {'cantidad': 2, 'precio_unitario': 2500.0},
        {'cantidad': 1, 'precio_unitario': 1000.0}
    ]
    
    resultado = calcular_totales(
        items=items,
        descuento_tipo='percent',
        descuento_valor=15.0,  # 15%
        iva_porcentaje=16.0,
        envio=500.0
    )
    
    # Subtotal: (3*5000) + (2*2500) + (1*1000) = 15000 + 5000 + 1000 = 21000
    assert resultado['subtotal'] == 21000.0
    # Descuento: 21000 * 0.15 = 3150
    assert resultado['descuento_monto'] == 3150.0
    # Base: 21000 - 3150 = 17850
    assert resultado['base_impuesto'] == 17850.0
    # IVA: 17850 * 0.16 = 2856
    assert resultado['iva_monto'] == 2856.0
    # Total: 17850 + 2856 + 500 = 21206
    assert resultado['total'] == 21206.0

def test_calcular_totales_items_vacios():
    """Test de cálculo sin items"""
    items = []
    
    resultado = calcular_totales(
        items=items,
        descuento_tipo='fixed',
        descuento_valor=0,
        iva_porcentaje=16.0,
        envio=0
    )
    
    assert resultado['subtotal'] == 0.0
    assert resultado['descuento_monto'] == 0.0
    assert resultado['base_impuesto'] == 0.0
    assert resultado['iva_monto'] == 0.0
    assert resultado['total'] == 0.0

def test_calcular_totales_descuento_mayor_que_subtotal():
    """Test cuando el descuento es mayor que el subtotal"""
    items = [
        {'cantidad': 1, 'precio_unitario': 100.0}
    ]
    
    resultado = calcular_totales(
        items=items,
        descuento_tipo='fixed',
        descuento_valor=200.0,  # Mayor que el subtotal
        iva_porcentaje=16.0,
        envio=0
    )
    
    assert resultado['subtotal'] == 100.0
    assert resultado['descuento_monto'] == 200.0
    # Base será negativa: 100 - 200 = -100
    assert resultado['base_impuesto'] == -100.0
    # IVA de base negativa: -100 * 0.16 = -16
    assert resultado['iva_monto'] == -16.0
    # Total: -100 + (-16) + 0 = -116
    assert resultado['total'] == -116.0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
