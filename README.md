# Sistema de Cotizaciones para Aire Acondicionado

Aplicación web completa en Python con arquitectura MVC para crear, editar, listar y exportar cotizaciones de equipos de aire acondicionado.

## Características

- ✅ Gestión completa de cotizaciones con cliente, items, descuentos e IVA
- ✅ Cálculo automático de subtotales, descuentos (porcentaje o fijo), IVA y total
- ✅ Exportación a Excel (.xlsx) con formato profesional
- ✅ Exportación a PDF listo para impresión
- ✅ Control de estado de pagos (Pendiente, Parcial, Pagado)
- ✅ Base de datos SQLite integrada
- ✅ Interfaz web responsive
- ✅ Tests unitarios incluidos

## Requisitos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd Punto_Adri
```

### 2. Crear entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota:** Si WeasyPrint falla al instalar (requiere GTK en Windows), la aplicación usará automáticamente ReportLab como alternativa para PDFs.

### 4. Inicializar la base de datos

```bash
python run.py
```

La base de datos se creará automáticamente al iniciar la aplicación por primera vez.

## Uso

### Iniciar la aplicación

```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

### Endpoints principales

- `GET /` - Lista de cotizaciones con filtros
- `GET /cotizacion/nueva` - Formulario para nueva cotización
- `POST /cotizacion` - Crear cotización
- `GET /cotizacion/<id>` - Ver cotización
- `GET /cotizacion/<id>/editar` - Editar cotización
- `POST /cotizacion/<id>/actualizar` - Actualizar cotización
- `GET /cotizacion/<id>/exportar/excel` - Descargar Excel
- `GET /cotizacion/<id>/exportar/pdf` - Descargar PDF
- `POST /cotizacion/<id>/pago` - Registrar pago

## Estructura del proyecto

```
Punto_Adri/
├── app/
│   ├── __init__.py          # Inicialización de Flask
│   ├── config.py            # Configuración de la aplicación
│   ├── models.py            # Modelos SQLAlchemy
│   ├── controllers.py       # Rutas y controladores
│   ├── utils.py             # Utilidades (cálculos, Excel, PDF)
│   ├── templates/           # Templates Jinja2
│   │   ├── base.html
│   │   ├── cotizacion_list.html
│   │   ├── cotizacion_form.html
│   │   └── cotizacion_printable.html
│   └── static/              # Archivos estáticos
│       ├── css/
│       │   └── print.css
│       └── logo.png (opcional)
├── tests/
│   └── test_calculos.py     # Tests unitarios
├── temp/                     # Archivos temporales (Excel/PDF)
├── cotizaciones.db          # Base de datos SQLite
├── requirements.txt         # Dependencias
├── run.py                   # Punto de entrada
└── README.md               # Este archivo
```

## Ejecutar tests

```bash
pytest tests/
```

O para ver más detalles:

```bash
pytest tests/ -v
```

## Configuración

Edita `app/config.py` para personalizar:

- Datos de la empresa (nombre, RFC, dirección, teléfono, email)
- Porcentaje de IVA (default 16%)
- Términos y condiciones
- Otras configuraciones

## Funcionalidades principales

### Crear cotización

1. Ingresar datos del cliente (opcional)
2. Agregar items con descripción, cantidad, unidad y precio
3. Aplicar descuento (porcentaje o monto fijo)
4. Configurar envío (opcional)
5. El sistema calcula automáticamente subtotal, IVA y total

### Exportar

- **Excel**: Formato profesional con encabezado, tabla de items, resumen y términos
- **PDF**: Documento listo para imprimir en tamaño carta

### Gestión de pagos

- Registrar pagos parciales o completos
- El sistema actualiza automáticamente el estado (Pendiente/Parcial/Pagado)
- Cálculo de saldo pendiente

## Fórmulas de cálculo

```
total_item = cantidad × precio_unitario
subtotal = Σ(total_item)
descuento_monto = subtotal × (descuento% / 100)  [si es porcentaje]
descuento_monto = valor_fijo  [si es monto fijo]
base_impuesto = subtotal - descuento_monto
iva_monto = base_impuesto × (iva% / 100)
total = base_impuesto + iva_monto + envío
saldo = total - monto_pagado
```

## Solución de problemas

### WeasyPrint no se instala en Windows

WeasyPrint requiere GTK. Si falla la instalación, la aplicación usará automáticamente ReportLab. Los PDFs se generarán correctamente con ambas librerías.

### Error de base de datos

Elimina `cotizaciones.db` y reinicia la aplicación para recrear la base de datos.

### Puerto 5000 en uso

Edita `run.py` y cambia el puerto:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Licencia

Este proyecto fue generado para uso interno de empresa de aire acondicionado.

## Soporte

Para problemas o sugerencias, contacta al administrador del sistema.
