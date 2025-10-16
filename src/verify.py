"""
verify.py
-----------------
Módulo encargado de verificar si un archivo PDF contiene una tabla con la estructura
esperada de una carga académica (columnas con los días Lunes–Viernes).

Usa `pdfplumber` para extraer la primera tabla y analizar sus encabezados, asi como el texto para validar.

Funciones principales:
    - verificar_pdf(pdf_bytes): valida la estructura y devuelve un reporte JSON.
"""
import pdfplumber
import io
import re

def verificar_pdf(pdf_bytes: bytes):
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for pagina in pdf.pages:
                tabla = pagina.extract_table()
                text = pagina.extract_text()
                if tabla and len(tabla) > 1 and re.search("CARGA ACADEMICA DEL ESTUDIANTE", text):
                    encabezados = [c.strip() for c in tabla[0] if c]
                    dias = {"Lunes", "Martes", "Miércoles", "Jueves", "Viernes"}
                    tiene_dias = dias.issubset(encabezados)

                    return {
                        "valido": [tiene_dias],
                        "encabezados_detectados": encabezados,
                        "mensaje": "Estructura válida" if tiene_dias else "No se detectaron todos los días requeridos"
                    }

        return {
            "valido": False,
            "encabezados_detectados": [],
            "mensaje": "No se detectaron tablas válidas en el PDF"
        }

    except Exception as e:
        return {"error": str(e)}