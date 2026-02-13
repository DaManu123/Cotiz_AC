# Manual de Usuario - Cotiz AC

## 📖 Índice
1. [Introducción](#introducción)
2. [Configuración Inicial](#configuración-inicial)
3. [Gestión de Clientes](#gestión-de-clientes)
4. [Crear Nueva Cotización](#crear-nueva-cotización)
5. [Historial de Cotizaciones](#historial-de-cotizaciones)
6. [Exportación de Documentos](#exportación-de-documentos)
7. [Consejos y Mejores Prácticas](#consejos-y-mejores-prácticas)

---

## Introducción

**Cotiz AC** es un sistema de gestión de cotizaciones diseñado específicamente para empresas de instalación y mantenimiento de aires acondicionados. Permite crear, gestionar y exportar cotizaciones profesionales de manera eficiente.

### Características Principales
- ✅ Generación automática de números consecutivos
- ✅ Gestión completa de clientes
- ✅ Cálculo automático de totales e impuestos
- ✅ Exportación a PDF y Excel
- ✅ Historial completo de cotizaciones
- ✅ Diseño profesional tipo ProForma

---

## Configuración Inicial

### Primer Uso

1. **Acceder al Sistema**
   - Abre tu navegador y ve a `http://localhost:5000`

2. **Configurar Datos de la Empresa**
   - Haz clic en "Configuración" en el menú superior
   - Completa los siguientes campos:
     - Nombre de la empresa
     - Dirección
     - Teléfono
     - Email
     - Redes sociales (opcional)
   - Haz clic en "Guardar Configuración"

> ⚠️ **Importante**: Los datos de la empresa aparecerán en todas las cotizaciones generadas.

---

## Gestión de Clientes

### Agregar Nuevo Cliente

1. Ve a la sección "Clientes" desde el menú
2. Haz clic en "Nuevo Cliente"
3. Completa el formulario:
   - **Nombre**: Requerido
   - **Teléfono**: Opcional
   - **Email**: Opcional
   - **Dirección**: Opcional
4. Haz clic en "Guardar"

### Editar Cliente

1. En la lista de clientes, haz clic en el botón de editar (icono de lápiz)
2. Modifica los campos necesarios
3. Haz clic en "Guardar"

### Eliminar Cliente

1. Haz clic en el botón de eliminar (icono de papelera)
2. Confirma la acción

> ⚠️ **Nota**: No se puede eliminar un cliente que tenga cotizaciones asociadas.

### Buscar Cliente

- Utiliza la barra de búsqueda para filtrar clientes por nombre
- La búsqueda es en tiempo real

---

## Crear Nueva Cotización

### Paso 1: Información General

1. Haz clic en "Nueva Cotización" desde el menú
2. El sistema asignará automáticamente:
   - Número de cotización consecutivo
   - Fecha actual (puedes modificarla)
3. Selecciona el estatus:
   - **Borrador**: Para cotizaciones en progreso
   - **Enviada**: Cuando se envía al cliente
   - **Aceptada**: Cliente aceptó la cotización
   - **Cancelada**: Cotización no procedió

### Paso 2: Seleccionar Cliente

1. Selecciona un cliente del menú desplegable
2. Los datos del cliente (teléfono y email) se mostrarán automáticamente
3. Si el cliente no existe:
   - Haz clic en "Nuevo"
   - Completa el formulario rápido
   - Guardar y continuar

### Paso 3: Agregar Conceptos

1. **Primera Línea**: El sistema crea automáticamente la primera línea
2. **Completar cada línea**:
   - **Cantidad**: Número de unidades
   - **Descripción**: Descripción detallada del servicio/producto
   - **Precio Unitario**: Costo por unidad
   - **Total**: Se calcula automáticamente

3. **Agregar más líneas**: Haz clic en "Agregar Línea"
4. **Eliminar líneas**: Haz clic en el icono de papelera

> 💡 **Tip**: Los totales se calculan automáticamente al ingresar cantidad y precio.

### Paso 4: Totales

El sistema calcula automáticamente:
- **Subtotal**: Suma de todas las líneas
- **IVA (16%)**: Calculado sobre el subtotal
- **Total**: Subtotal + IVA

### Paso 5: Notas y Condiciones

- Agrega información adicional como:
  - Garantías
  - Tiempo de entrega
  - Condiciones de pago
  - Validez de la cotización

### Paso 6: Guardar

1. Haz clic en "Guardar Cotización"
2. El sistema te preguntará si deseas descargar el PDF
3. La cotización se guardará en la base de datos

---

## Historial de Cotizaciones

### Ver Todas las Cotizaciones

1. Ve a "Historial" desde el menú
2. Visualiza todas las cotizaciones en la tabla

### Filtrar Cotizaciones

Utiliza los filtros disponibles:
- **Por Cliente**: Selecciona un cliente específico
- **Por Estatus**: Filtra por estado (Borrador, Enviada, etc.)
- **Por Fecha**: Define un rango de fechas
- Haz clic en "Buscar" para aplicar filtros

### Ver Detalle

1. Haz clic en el icono de ojo (👁️) en cualquier cotización
2. Se mostrará una ventana con:
   - Información completa de la cotización
   - Datos del cliente
   - Todos los conceptos
   - Totales calculados
   - Notas

### Exportar Cotización

Desde el historial puedes:
- **PDF**: Haz clic en el icono de PDF (rojo)
- **Excel**: Haz clic en el icono de Excel (verde)

> 💡 **Tip**: Los archivos se descargan automáticamente con un formato profesional.

### Eliminar Cotización

1. Haz clic en el icono de papelera
2. Confirma la eliminación
3. **⚠️ Esta acción no se puede deshacer**

---

## Exportación de Documentos

### Formato PDF

**Características del PDF generado**:
- Encabezado con datos de la empresa
- Número de cotización y fecha
- Información del cliente
- Tabla profesional de conceptos
- Cálculo de totales destacado
- Notas y condiciones
- Pie de página con fecha de generación

**Uso recomendado**: Para enviar al cliente por email o imprimir

### Formato Excel

**Características del Excel generado**:
- Mismo diseño visual que PDF
- Editable en Microsoft Excel u OpenOffice
- Formato de moneda aplicado
- Colores y estilos profesionales

**Uso recomendado**: Cuando el cliente necesita editar o tiene plantillas propias

---

## Consejos y Mejores Prácticas

### ✅ Buenas Prácticas

1. **Registro de Clientes**
   - Mantén actualizada la información de contacto
   - Registra clientes antes de crear cotizaciones

2. **Descripciones Claras**
   - Sé específico en las descripciones de conceptos
   - Incluye marcas, modelos y especificaciones

3. **Notas Detalladas**
   - Especifica garantías y condiciones
   - Define tiempo de entrega
   - Menciona validez de la cotización

4. **Gestión de Estatus**
   - Actualiza el estatus conforme avanza el proceso
   - Usa "Borrador" mientras trabajas en ella
   - Cambia a "Enviada" al enviarla al cliente

5. **Backup Regular**
   - Haz copias de seguridad del archivo `cotizaciones.db`
   - Guarda versiones importantes en carpeta separada

### 🎯 Flujo de Trabajo Recomendado

1. **Recepción de Solicitud**
   - Crear/Verificar cliente en el sistema
   - Crear nueva cotización en estatus "Borrador"

2. **Elaboración**
   - Agregar conceptos con precios actualizados
   - Incluir todas las notas relevantes
   - Revisar totales

3. **Envío**
   - Cambiar estatus a "Enviada"
   - Exportar a PDF
   - Enviar por email al cliente

4. **Seguimiento**
   - Actualizar estatus según respuesta del cliente
   - Convertir a "Aceptada" si el cliente acepta
   - Marcar como "Cancelada" si no procede

### 💡 Atajos y Tips

- **Búsqueda rápida**: Usa la barra de búsqueda en clientes
- **Filtros avanzados**: Combina múltiples filtros en el historial
- **Copiar conceptos**: Puedes copiar descripciones de cotizaciones anteriores
- **Dashboard**: Usa el dashboard para ver estadísticas rápidas

---

## Soporte y Ayuda

### Problemas Comunes

**No puedo guardar una cotización**
- Verifica que hayas seleccionado un cliente
- Asegúrate de tener al menos un concepto
- Revisa que todos los campos requeridos estén completos

**No se generan los PDFs**
- Verifica que el directorio `exports/pdf` existe
- Revisa los permisos de escritura

**Los cálculos no son correctos**
- El sistema calcula IVA al 16% automáticamente
- Verifica que los precios unitarios sean correctos

### Contacto

Para soporte técnico adicional, contacta al administrador del sistema.

---

## Actualizaciones Futuras

El sistema está diseñado para crecer. Próximas funcionalidades planeadas:
- Conversión automática a factura
- Envío por correo desde el sistema
- Firma digital de cotizaciones
- Catálogo de productos/servicios precargados
- Control de pagos
- Reportes financieros avanzados
- Dashboard de ventas

---

**Versión del Manual**: 1.0  
**Fecha**: Febrero 2026  
**Sistema**: Cotiz AC v1.0
