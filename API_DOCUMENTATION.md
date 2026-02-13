# API Documentation - Cotiz AC

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### Cotizaciones

#### GET /cotizaciones
Obtiene todas las cotizaciones con filtros opcionales.

**Query Parameters:**
- `cliente_id` (optional): Filtrar por cliente
- `estatus` (optional): Filtrar por estatus
- `fecha_desde` (optional): Fecha inicio (YYYY-MM-DD)
- `fecha_hasta` (optional): Fecha fin (YYYY-MM-DD)

**Response:**
```json
{
  "cotizaciones": [
    {
      "id": 1,
      "numero_cotizacion": "COT-00001",
      "fecha": "2026-02-11",
      "cliente_id": 1,
      "cliente": {...},
      "subtotal": 22000.00,
      "impuestos": 3520.00,
      "total": 25520.00,
      "estatus": "Enviada",
      "notas": "...",
      "detalles": [...]
    }
  ],
  "total": 1
}
```

#### GET /cotizaciones/:id
Obtiene una cotización específica.

**Response:**
```json
{
  "cotizacion": {
    "id": 1,
    "numero_cotizacion": "COT-00001",
    ...
  }
}
```

#### POST /cotizaciones
Crea una nueva cotización.

**Request Body:**
```json
{
  "cliente_id": 1,
  "fecha": "2026-02-11",
  "notas": "Incluye garantía",
  "detalles": [
    {
      "cantidad": 2,
      "descripcion": "Aire Acondicionado 12,000 BTU",
      "precio_unitario": 8500.00
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "cotizacion": {...}
}
```

#### PUT /cotizaciones/:id
Actualiza una cotización existente.

#### DELETE /cotizaciones/:id
Elimina una cotización.

#### PATCH /cotizaciones/:id/estatus
Cambia el estatus de una cotización.

**Request Body:**
```json
{
  "estatus": "Aceptada"
}
```

#### GET /cotizaciones/consecutivo
Obtiene el siguiente número consecutivo.

**Response:**
```json
{
  "numero_cotizacion": "COT-00002"
}
```

#### GET /cotizaciones/:id/export/pdf
Descarga la cotización en formato PDF.

#### GET /cotizaciones/:id/export/excel
Descarga la cotización en formato Excel.

---

### Clientes

#### GET /clientes
Obtiene todos los clientes.

**Query Parameters:**
- `busqueda` (optional): Buscar por nombre

**Response:**
```json
{
  "clientes": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "telefono": "555-1111",
      "email": "juan@email.com",
      "direccion": "Calle 123"
    }
  ],
  "total": 1
}
```

#### GET /clientes/:id
Obtiene un cliente específico.

#### POST /clientes
Crea un nuevo cliente.

**Request Body:**
```json
{
  "nombre": "María López",
  "telefono": "555-2222",
  "email": "maria@email.com",
  "direccion": "Av. Principal 456"
}
```

#### PUT /clientes/:id
Actualiza un cliente existente.

#### DELETE /clientes/:id
Elimina un cliente (solo si no tiene cotizaciones).

---

### Empresa

#### GET /empresa
Obtiene los datos de la empresa.

**Response:**
```json
{
  "empresa": {
    "id": 1,
    "nombre": "Cotiz AC",
    "direccion": "Av. Principal 123",
    "telefono": "(555) 123-4567",
    "email": "contacto@cotizac.com",
    "redes_sociales": "Facebook: @CotizAC"
  }
}
```

#### POST /empresa
Crea o actualiza datos de la empresa.

**Request Body:**
```json
{
  "nombre": "Mi Empresa AC",
  "direccion": "Calle Nueva 789",
  "telefono": "555-9999",
  "email": "info@miempresa.com",
  "redes_sociales": "Instagram: @miempresa"
}
```

---

## Códigos de Estado HTTP

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Datos inválidos
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Errores

Formato de respuesta de error:
```json
{
  "error": "Mensaje descriptivo del error"
}
```
