"""
process.py
----------------
Módulo encargado de procesar un archivo PDF que contiene una carga académica
(tabla con los días Lunes–Viernes y sus respectivos horarios).

Extrae los horarios, los ordena y devuelve un JSON con los **espacios disponibles**
entre clases de cada día.

Dependencias:
    - pdfplumber
    - pandas
    - re

Funciones principales:
    - procesar_pdf(pdf_bytes): procesa un PDF en bytes y retorna los horarios libres por día.
"""
import io
import pdfplumber
import pandas as pd
import re

def parse_interval(horario):
    """
    Convierte una cadena de horario (por ejemplo: "07:00 - 09:00")
    en un par de minutos enteros (inicio, fin).

    Args:
        horario (str): Texto del horario a analizar.

    Returns:
        tuple[int, int] | None: (inicio_minutos, fin_minutos) o None si el formato no coincide.
    """
    
    match = re.findall(r"(\d{1,2}):(\d{2})", str(horario))
    if len(match) >= 2:
        start_h, start_m = map(int, match[0])
        end_h, end_m = map(int, match[1])
        return start_h * 60 + start_m, end_h * 60 + end_m
    return None

def min_to_str(m):
    """
    Convierte minutos enteros a formato HH:MM.

    Args:
        m (int): Minutos desde medianoche.

    Returns:
        str: Hora formateada (por ejemplo: '07:00')
    """
    return f"{m // 60:02d}:{m % 60:02d}"

def procesar_pdf(pdf_bytes: bytes):
    """
    Procesa un PDF de carga académica y obtiene los horarios disponibles
    (espacios libres entre clases) para cada día de la semana.

    Args:
        pdf_bytes (bytes): Contenido binario del archivo PDF.

    Returns:
        dict: Diccionario con los días como claves y listas de horarios libres como valores.
              Ejemplo:
              {
                  "lunes": ["09:00 - 11:00", "13:00 - 15:00"],
                  "martes": [],
                  ...
              }
    """
    filas = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for pagina in pdf.pages:
            tabla = pagina.extract_table()
            if tabla:
                for fila in tabla:
                    filas.append(fila)

    if not filas:
        return {"error": "No se detectaron tablas en el PDF"}

    df = pd.DataFrame(filas[1:], columns=filas[0])
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    df_dias = df[dias]
    horarios_dias = {dia: df_dias[dia].dropna().tolist() for dia in dias}

    disponibles = {}
    for dia, horarios in horarios_dias.items():
        intervals = [parse_interval(h) for h in horarios if parse_interval(h)]
        if not intervals:
            disponibles[dia.lower()] = []
            continue

        intervals.sort(key=lambda x: x[0])
        libres = []
        for i in range(len(intervals) - 1):
            fin_actual = intervals[i][1]
            inicio_sig = intervals[i + 1][0]
            if inicio_sig > fin_actual:
                libres.append(f"{min_to_str(fin_actual)} - {min_to_str(inicio_sig)}")
        disponibles[dia.lower()] = libres

    return disponibles
