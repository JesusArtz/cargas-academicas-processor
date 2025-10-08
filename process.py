# procesar_pdf.py
import io
import pdfplumber
import pandas as pd
import re

def parse_interval(horario):
    match = re.findall(r"(\d{1,2}):(\d{2})", str(horario))
    if len(match) >= 2:
        start_h, start_m = map(int, match[0])
        end_h, end_m = map(int, match[1])
        return start_h * 60 + start_m, end_h * 60 + end_m
    return None

def min_to_str(m):
    return f"{m // 60:02d}:{m % 60:02d}"

def procesar_pdf(pdf_bytes: bytes):
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
