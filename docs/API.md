# Referencia de la API REST

## Convenciones

- Las respuestas de la API se devuelven en JSON.
- Las solicitudes de creación y actualización deben enviarse con `Content-Type: application/json`.
- El tamaño máximo configurado del cuerpo de solicitud es de 16 KiB.
- `product_id` es un identificador entero en la ruta.

## Endpoints

### `GET /products`

Obtiene todos los productos. No requiere cuerpo ni parámetros de consulta definidos por la ruta.

**Respuesta: `200 OK`**

```json
[
  {
    "id": 1,
    "name": "Ejemplo",
    "price": 125.0,
    "description": "Descripción del producto"
  }
]
```

La respuesta es una lista; si no hay productos, se espera una lista vacía.

### `GET /products/{product_id}`

Obtiene un producto por su identificador entero.

**Respuesta: `200 OK`**

```json
{
  "id": 1,
  "name": "Ejemplo",
  "price": 125.0,
  "description": "Descripción del producto"
}
```

**Errores:** `404 Not Found` si el producto no existe; `500 Internal Server Error` si falla la consulta.

### `POST /products`

Crea un producto.

**Cuerpo JSON requerido:**

```json
{
  "name": "Ejemplo",
  "price": 125.0,
  "description": "Descripción del producto"
}
```

Reglas de validación:

- `name`: cadena obligatoria de 1 a 30 caracteres.
- `price`: número mayor que cero, no superior a `99999999.99`; no admite NaN ni infinito.
- `description`: cadena obligatoria de 1 a 255 caracteres.
- Se eliminan espacios al inicio y al final de las cadenas.
- No se permiten campos adicionales.

**Respuesta: `201 Created`**. Devuelve el producto creado, incluido su identificador.

**Errores:** `400 Bad Request` para JSON o datos inválidos; `409 Conflict` para conflictos de duplicidad; `415 Unsupported Media Type` si el tipo de contenido no es compatible; `500 Internal Server Error` ante errores internos.

### `PUT /products/{product_id}`

Sustituye los datos de un producto. **Es una actualización completa, no parcial**: requiere `name`, `price` y `description`, con las mismas reglas de validación que `POST /products`.

**Respuesta: `200 OK`**. Devuelve el producto actualizado.

**Errores:** `400 Bad Request`, `404 Not Found`, `409 Conflict`, `415 Unsupported Media Type` o `500 Internal Server Error`, según el caso.

### `DELETE /products/{product_id}`

Elimina un producto por su identificador entero.

**Respuesta: `200 OK`**

```json
{
  "message": "Producto eliminado"
}
```

**Errores:** `404 Not Found` si no existe; `500 Internal Server Error` si falla la operación.

## Formato de errores

Los errores se devuelven como objetos JSON. Para errores generales, la estructura es:

```json
{
  "error": "Mensaje del error"
}
```

Los errores de validación de Pydantic incluyen `error` y `details`. Cada elemento de `details` puede incluir `field`, `message` y `type`. Los mensajes y tipos concretos dependen de la validación que haya fallado.

La aplicación contempla, entre otros, los códigos HTTP 400, 404, 409, 413, 415, 500 y 503. Los errores internos no deben exponer credenciales ni información sensible de la base de datos.

## Rutas deshabilitadas

- `GET /admin`: devuelve `503 Service Unavailable` hasta implementar autenticación.
- `POST /login`: devuelve `503 Service Unavailable` hasta implementar autenticación.

Estas rutas no constituyen un sistema de autenticación funcional.

## Consideraciones

No se documentan parámetros de paginación, filtros ni ordenamiento porque no están definidos en las rutas revisadas. Actualiza esta referencia y las pruebas relacionadas cuando cambie el comportamiento de la API.
