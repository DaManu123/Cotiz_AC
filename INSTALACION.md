# Guía de Instalación - Cotiz AC

## 🚀 Requisitos Previos

Antes de instalar Cotiz AC, asegúrate de tener:

- **Python 3.8 o superior** instalado
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)
- **Navegador web moderno** (Chrome, Firefox, Edge)

---

## 📦 Instalación Paso a Paso

### 1. Descargar el Proyecto

**Opción A: Si tienes Git**
```bash
git clone https://github.com/tu-usuario/Cotiz_AC.git
cd Cotiz_AC
```

**Opción B: Descarga manual**
1. Descarga el archivo ZIP del proyecto
2. Extrae el contenido en una carpeta
3. Abre la terminal en esa carpeta

### 2. Crear Entorno Virtual

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 **Nota**: Verás `(venv)` al inicio de tu línea de comandos cuando el entorno esté activado.

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará todas las librerías necesarias:
- Flask (framework web)
- SQLAlchemy (base de datos)
- ReportLab (generación de PDFs)
- OpenPyXL (generación de Excel)
- Y otras dependencias

### 4. Inicializar Base de Datos

```bash
python init_db.py
```

Este comando:
- Crea la base de datos SQLite
- Crea todas las tablas necesarias
- Inserta datos de ejemplo (empresa, clientes, cotización de prueba)

Deberías ver un mensaje como:
```
✅ Base de datos inicializada correctamente!
✅ Empresa creada: Cotiz AC - Servicios de Climatización
✅ 3 clientes creados
✅ 1 cotización de ejemplo creada: COT-00001
```

### 5. Iniciar el Servidor

```bash
flask run
```

O también:
```bash
python app.py
```

Verás un mensaje como:
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.X:5000
```

### 6. Acceder al Sistema

Abre tu navegador y ve a:
```
http://localhost:5000
```

¡Listo! El sistema está funcionando.

---

## 🔧 Configuración Inicial

### Primera Vez

1. **Ir a Configuración**
   - Haz clic en "Configuración" en el menú superior
   
2. **Actualizar Datos de Empresa**
   - Modifica los datos de ejemplo con tu información real:
     - Nombre de tu empresa
     - Dirección
     - Teléfono
     - Email
     - Redes sociales
   - Guardar

3. **Revisar Clientes de Ejemplo**
   - Ve a "Clientes"
   - Elimina o modifica los clientes de ejemplo
   - Agrega tus clientes reales

4. **Probar con Cotización de Ejemplo**
   - Ve a "Historial"
   - Revisa la cotización de ejemplo (COT-00001)
   - Descarga el PDF para ver el formato
   - Elimínala si no la necesitas

---

## 🗄️ Estructura de Archivos Generados

Después de la instalación, verás esta estructura:

```
Cotiz_AC/
├── venv/                    # Entorno virtual (no tocar)
├── exports/                 # Archivos generados
│   ├── pdf/                # PDFs de cotizaciones
│   └── excel/              # Excels de cotizaciones
├── cotizaciones.db         # Base de datos SQLite
└── ... (otros archivos del proyecto)
```

---

## 🔐 Configuración Avanzada (Opcional)

### Variables de Entorno

El archivo `.env` contiene configuraciones:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///cotizaciones.db
```

**Para producción, cambia:**
- `FLASK_ENV=production`
- `SECRET_KEY=tu-clave-secreta-aleatoria`

### Cambiar Puerto

Por defecto usa el puerto 5000. Para cambiarlo:

**Opción 1: Modificar app.py**
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

**Opción 2: Variable de entorno**
```bash
flask run --port=8080
```

### Acceso desde Otros Dispositivos

El servidor por defecto es accesible desde toda la red local.

1. Encuentra tu IP local:
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig` o `ip addr`

2. Desde otro dispositivo en la misma red:
   ```
   http://TU_IP_LOCAL:5000
   ```

---

## 🐛 Solución de Problemas

### Error: "Python no se reconoce"

**Solución**: Python no está instalado o no está en PATH
1. Descarga Python desde python.org
2. Durante la instalación, marca "Add Python to PATH"
3. Reinicia la terminal

### Error: "pip no se reconoce"

**Solución**:
```bash
python -m pip install -r requirements.txt
```

### Error: "No module named 'flask'"

**Solución**: El entorno virtual no está activado
1. Activa el entorno virtual:
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```
2. Reinstala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Error al ejecutar scripts en Windows

**Solución**: Habilitar ejecución de scripts
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Puerto 5000 ya en uso

**Solución**: Cambiar puerto
```bash
flask run --port=8080
```

### Base de datos bloqueada

**Solución**: Cierra todas las instancias del servidor
```bash
# Buscar procesos Python
tasklist | findstr python

# Matar proceso específico (Windows)
taskkill /PID numero_pid /F
```

---

## 🔄 Actualizar el Sistema

### Actualizar Dependencias

```bash
pip install --upgrade -r requirements.txt
```

### Reset de Base de Datos

**⚠️ ADVERTENCIA: Esto eliminará todos los datos**

```bash
# Windows
del cotizaciones.db
python init_db.py

# Linux/Mac
rm cotizaciones.db
python init_db.py
```

---

## 💾 Backup y Restauración

### Hacer Backup

**Importante**: Respalda estos archivos:

1. **Base de datos**:
   ```bash
   # Copiar archivo de base de datos
   copy cotizaciones.db cotizaciones_backup_FECHA.db
   ```

2. **Cotizaciones generadas**:
   ```bash
   # Respaldar carpeta completa
   xcopy exports exports_backup /E /I
   ```

### Restaurar Backup

1. Detén el servidor
2. Reemplaza `cotizaciones.db` con tu backup
3. Reinicia el servidor

---

## 🌐 Despliegue en Producción (Avanzado)

### Opción 1: Servidor Local (Windows/Linux)

1. Instalar como servicio de Windows/systemd
2. Usar Waitress o Gunicorn como servidor WSGI
3. Configurar firewall

### Opción 2: Hosting Web

Plataformas recomendadas:
- **Heroku** (gratuito para empezar)
- **PythonAnywhere**
- **DigitalOcean**
- **AWS/Azure**

### Opción 3: Docker (Avanzado)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## 📱 Acceso Móvil

El sistema es totalmente responsive y funciona en:
- ✅ Smartphones
- ✅ Tablets
- ✅ Computadoras de escritorio

Solo accede desde el navegador móvil usando la URL del servidor.

---

## 🆘 Obtener Ayuda

Si tienes problemas:

1. **Verifica los logs de la terminal** donde corre Flask
2. **Revisa el navegador** - presiona F12 para ver errores en consola
3. **Consulta el archivo README.md** para información adicional
4. **Revisa que todas las dependencias estén instaladas**

---

## ✅ Checklist de Instalación

- [ ] Python instalado (3.8+)
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas sin errores
- [ ] Base de datos inicializada correctamente
- [ ] Servidor Flask corriendo
- [ ] Acceso al sistema desde navegador
- [ ] Datos de empresa configurados
- [ ] Primera cotización de prueba creada

---

**¡Felicidades! Ya tienes Cotiz AC funcionando.**

Para aprender a usar el sistema, consulta el [Manual de Usuario](MANUAL_USUARIO.md).
