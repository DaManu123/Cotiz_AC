# 🚀 Inicio Rápido - Cotiz AC

## ⚡ Comandos Esenciales

### Activar Entorno Virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

---

### Iniciar el Servidor

```bash
python app.py
```

O usando Flask CLI:
```bash
flask run
```

**Acceder al sistema:**
```
http://localhost:5000
```

---

### Reiniciar Base de Datos

**⚠️ ADVERTENCIA: Esto borrará todos los datos**

**Windows:**
```powershell
Remove-Item cotizaciones.db -ErrorAction SilentlyContinue
python init_db.py
```

**Linux/Mac:**
```bash
rm -f cotizaciones.db
python init_db.py
```

---

### Instalar/Actualizar Dependencias

```bash
pip install -r requirements.txt
```

---

## 🔍 Verificación Rápida

### Verificar que todo funciona:

1. **Base de datos existe:**
   ```bash
   ls cotizaciones.db  # Linux/Mac
   dir cotizaciones.db  # Windows
   ```

2. **Servidor corriendo:**
   - Abre http://localhost:5000
   - Deberías ver el Dashboard

3. **Probar funcionalidades:**
   - Dashboard: http://localhost:5000/
   - Nueva Cotización: http://localhost:5000/nueva-cotizacion
   - Historial: http://localhost:5000/historial
   - Clientes: http://localhost:5000/clientes
   - Configuración: http://localhost:5000/configuracion

---

## 📁 Estructura de Directorios Importante

```
Cotiz_AC/
├── venv/                    # ⚠️ NO TOCAR - Entorno virtual
├── src/
│   ├── models/             # Modelos de BD
│   ├── controllers/        # Lógica de negocio
│   └── services/           # PDF y Excel
├── templates/              # Plantillas HTML
├── static/                 # CSS y JavaScript
│   ├── css/
│   └── js/
├── exports/                # 📄 Cotizaciones generadas
│   ├── pdf/
│   └── excel/
├── cotizaciones.db         # 🗄️ Base de datos
├── app.py                  # 🚀 Aplicación principal
└── init_db.py              # 🔧 Script de inicialización
```

---

## 🐛 Solución Rápida de Problemas

### Servidor no inicia
```bash
# Verificar que el entorno virtual está activado
# Debe aparecer (venv) al inicio de la línea

# Si no está activado:
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac
```

### Puerto 5000 ocupado
```bash
# Usar otro puerto
flask run --port=8080
```

### Cambios no se reflejan
```bash
# Reiniciar el servidor
# Presiona Ctrl+C y ejecuta nuevamente:
python app.py
```

### Error de importación
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

---

## 🎯 Flujo de Desarrollo

### 1. Iniciar sesión de trabajo
```bash
# Abrir terminal en la carpeta del proyecto
cd Cotiz_AC

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar servidor
python app.py
```

### 2. Durante el desarrollo
- El servidor se recarga automáticamente al guardar cambios
- Presiona F12 en el navegador para ver errores de JavaScript
- Revisa la terminal para errores de Python

### 3. Terminar sesión
```bash
# Presiona Ctrl+C para detener el servidor
# Desactivar entorno virtual
deactivate
```

---

## 📊 Endpoints API Rápidos

### Cotizaciones
- GET /api/cotizaciones - Lista todas
- POST /api/cotizaciones - Crear nueva
- GET /api/cotizaciones/:id - Ver detalle
- PUT /api/cotizaciones/:id - Actualizar
- DELETE /api/cotizaciones/:id - Eliminar
- GET /api/cotizaciones/:id/export/pdf - Descargar PDF
- GET /api/cotizaciones/:id/export/excel - Descargar Excel

### Clientes
- GET /api/clientes - Lista todos
- POST /api/clientes - Crear nuevo
- GET /api/clientes/:id - Ver detalle
- PUT /api/clientes/:id - Actualizar
- DELETE /api/clientes/:id - Eliminar

### Empresa
- GET /api/empresa - Obtener datos
- POST /api/empresa - Guardar/actualizar

---

## 💡 Tips de Desarrollo

### Ver logs en tiempo real
Los logs aparecen en la terminal donde corre el servidor.

### Probar API con cURL
```bash
# Obtener todas las cotizaciones
curl http://localhost:5000/api/cotizaciones

# Crear cliente
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Test Cliente", "telefono": "555-1234"}'
```

### Backup rápido
```bash
# Copiar base de datos
copy cotizaciones.db backup\cotizaciones_$(date +%Y%m%d).db
```

---

## 🚀 Producción (Checklist)

Antes de poner en producción:

- [ ] Cambiar SECRET_KEY en .env
- [ ] Cambiar FLASK_ENV=production
- [ ] Usar un servidor WSGI (Waitress, Gunicorn)
- [ ] Configurar base de datos PostgreSQL (opcional)
- [ ] Hacer backup de datos
- [ ] Configurar HTTPS
- [ ] Probar todas las funcionalidades

---

## 📞 Comandos Útiles Adicionales

### Ver versión de Python
```bash
python --version
```

### Ver paquetes instalados
```bash
pip list
```

### Actualizar pip
```bash
python -m pip install --upgrade pip
```

### Limpiar archivos cache
```bash
# Windows
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force

# Linux/Mac
find . -type d -name "__pycache__" -exec rm -r {} +
```

---

**¡Estás listo para desarrollar! 🎉**

Para más información detallada, consulta:
- [README.md](README.md) - Información general
- [INSTALACION.md](INSTALACION.md) - Guía completa de instalación
- [MANUAL_USUARIO.md](MANUAL_USUARIO.md) - Manual de usuario
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Documentación de API
