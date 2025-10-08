
import pdfplumber
import io

def verificar_pdf(pdf_bytes: bytes):
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for pagina in pdf.pages:
                tabla = pagina.extract_table()
                if tabla and len(tabla) > 1:
                    encabezados = [c.strip() for c in tabla[0] if c]
                    dias = {"Lunes", "Martes", "Miércoles", "Jueves", "Viernes"}
                    tiene_dias = dias.issubset(encabezados)

                    return {
                        "valido": tiene_dias,
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