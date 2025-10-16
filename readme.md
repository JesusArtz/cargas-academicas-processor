# Documentación de la API de Procesamiento y Verificación de PDFs

Esta API permite procesar y verificar archivos PDF que contienen cargas académicas (tablas con días Lunes–Viernes y horarios). Devuelve información sobre los espacios libres entre clases y valida la estructura de las tablas.

---

## Endpoints

| Endpoint | Método | Request | Response | Notas |
|----------|--------|---------|----------|-------|
| `/` | `GET` | Ninguno | `200 OK` <br> `"hello"` | Endpoint principal para verificar que la API está funcionando. |
| `/procesar_pdf` | `POST` | ```json { "pdf_b64": "<PDF codificado en base64>" } ``` | **Éxito:** <br> `200 OK` <br> ```json { "lunes": ["09:00 - 11:00"], "martes": [], "miércoles": ["10:00 - 12:00"], "jueves": [], "viernes": ["08:00 - 09:00"] } ``` <br> **Error PDF no recibido:** <br> `400 Bad Request` <br> ```json { "error": "No se recibió PDF en base64" } ``` <br> **Error interno:** <br> `500 Internal Server Error` <br> ```json { "error": "No se detectaron tablas en el PDF" } ``` | Procesa un PDF de carga académica y devuelve los horarios disponibles (espacios libres entre clases). <br> Las claves son los días en minúsculas y los valores son listas de intervalos `"HH:MM - HH:MM"`. |
| `/verificar_pdf` | `POST` | ```json { "pdf_b64": "<PDF codificado en base64>" } ``` | **Éxito:** <br> `200 OK` <br> Válido: <br> ```json { "valido": true, "encabezados_detectados": ["Lunes","Martes","Miércoles","Jueves","Viernes"], "mensaje": "Estructura válida" } ``` <br> No válido: <br> ```json { "valido": false, "encabezados_detectados": ["Lunes","Martes","Jueves","Viernes"], "mensaje": "No se detectaron todos los días requeridos" } ``` <br> **Error PDF no recibido:** <br> `400 Bad Request` <br> ```json { "error": "No se recibió PDF en base64" } ``` <br> **Error interno:** <br> `500 Internal Server Error` <br> ```json { "error": "mensaje de la excepción" } ``` | Verifica que el PDF tenga una tabla con la estructura esperada de carga académica. Retorna si es válido o no y los encabezados detectados. |

---


