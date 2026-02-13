# Sistema de Gestión de Cotizaciones - Cotiz_AC

Sistema completo de generación y gestión de cotizaciones para empresa de instalación y mantenimiento de aires acondicionados.

## 🚀 Características

- ✅ Generación automática de cotizaciones con consecutivo
- ✅ Gestión de clientes
- ✅ Base de datos relacional (SQLite/PostgreSQL)
- ✅ Exportación a PDF y Excel
- ✅ Diseño profesional tipo ProForma
- ✅ Cálculo automático de totales
- ✅ Historial y consulta de cotizaciones
- ✅ Arquitectura modular y escalable

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. Clonar el repositorio o descargar los archivos

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Inicializar base de datos:
```bash
python init_db.py
```

## 🚀 Uso

1. Iniciar el servidor:
```bash
flask run
```

2. Abrir navegador en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
Cotiz_AC/
├── src/
│   ├── models/          # Modelos de base de datos
│   ├── controllers/     # Controladores de lógica de negocio
│   ├── services/        # Servicios (PDF, Excel)
│   └── utils/           # Utilidades
├── templates/           # Plantillas HTML
├── static/             # Archivos estáticos (CSS, JS)
├── database/           # Migraciones
├── exports/            # PDFs y Excels generados
├── app.py              # Aplicación principal
└── requirements.txt    # Dependencias
```

## 🗄️ Modelo de Datos

- **Empresa**: Datos de la empresa
- **Cliente**: Información de clientes
- **Cotizacion**: Encabezado de cotizaciones
- **DetalleCotizacion**: Líneas de conceptos

## 📊 Roadmap Futuro

- [ ] Conversión a factura
- [ ] Envío automático por correo
- [ ] Firma digital
- [ ] Catálogo de servicios
- [ ] Control de pagos
- [ ] Reportes financieros
- [ ] Dashboard analítico

## 👨‍💻 Autor

Desarrollado para empresa de Aires Acondicionados
