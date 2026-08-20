"""
Generador de Análisis de Recursos
Lee la hoja 'Recursos' del Excel fuente y genera análisis de asignación y carga.
"""
import sys
import os
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.rutas import (
    ARCHIVO_FUENTE, ARCHIVO_SALIDA_REPORTE, MAPEO_RECURSOS,
    FASES_RECURSO, HH_DIARIAS, BRANDING
)

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Colores
FILL_HEADER = PatternFill(start_color="FF333F48", end_color="FF333F48", fill_type="solid")
FILL_SOBRECARGA = PatternFill(start_color="FFFF4444", end_color="FFFF4444", fill_type="solid")
FILL_ALTA = PatternFill(start_color="FFFF8C00", end_color="FFFF8C00", fill_type="solid")
FILL_MEDIA = PatternFill(start_color="FFFFD700", end_color="FFFFD700", fill_type="solid")
FILL_BAJA = PatternFill(start_color="FF90EE90", end_color="FF90EE90", fill_type="solid")
FILL_COLA = PatternFill(start_color="FFE8E8E8", end_color="FFE8E8E8", fill_type="solid")
FILL_DESARROLLO = PatternFill(start_color="FFFFCC", end_color="FFFFCC", fill_type="solid")
FILL_QA = PatternFill(start_color="CCE5FF", end_color="CCE5FF", fill_type="solid")
FILL_PRODUCCION = PatternFill(start_color="CCFFCC", end_color="CCFFCC", fill_type="solid")

FONT_HEADER = Font(name="Calibri", size=9, bold=True, color="FFFFFFFF")
FONT_BODY = Font(name="Calibri", size=9)
FONT_TITULO = Font(name="Calibri", size=16, bold=True, color="FF333F48")
FONT_SECCION = Font(name="Calibri", size=11, bold=True)

ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
THIN_BORDER = Border(
    left=Side(style="thin", color="FFB0B0B0"),
    right=Side(style="thin", color="FFB0B0B0"),
    top=Side(style="thin", color="FFB0B0B0"),
    bottom=Side(style="thin", color="FFB0B0B0"),
)

FASE_FILL_MAP = {
    "Cola": FILL_COLA,
    "Desarrollo": FILL_DESARROLLO,
    "QA": FILL_QA,
    "Producción": FILL_PRODUCCION,
}


def leer_recursos():
    """Lee la hoja 'Recursos' del Excel fuente."""
    try:
        wb = openpyxl.load_workbook(ARCHIVO_FUENTE, read_only=True)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ARCHIVO_FUENTE}")
        return []

    if "Recursos" not in wb.sheetnames:
        print("Hoja 'Recursos' no encontrada en el Excel.")
        wb.close()
        return []

    ws = wb["Recursos"]
    m = MAPEO_RECURSOS
    recursos = []

    for r in range(2, ws.max_row + 1):
        valores = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
        if all(v is None for v in valores):
            continue

        recurso = {
            "persona": valores[m["persona"]] if len(valores) > m["persona"] else "",
            "horas_estimadas": valores[m["horas_estimadas"]] if len(valores) > m["horas_estimadas"] else 0,
            "horas_reales": valores[m["horas_reales"]] if len(valores) > m["horas_reales"] else 0,
            "capacidad_semanal": valores[m["capacidad_semanal"]] if len(valores) > m["capacidad_semanal"] else 40,
            "fase_actual": valores[m["fase_actual"]] if len(valores) > m["fase_actual"] else "",
            "asignado_a": valores[m["asignado_a"]] if len(valores) > m["asignado_a"] else "",
        }
        recursos.append(recurso)

    wb.close()
    return recursos


def calcular_metricas(recursos):
    """Calcula métricas de recursos."""
    total = len(recursos)
    if total == 0:
        return {
            "total": 0, "total_horas_estimadas": 0, "total_horas_reales": 0,
            "promedio_utilizacion": 0, "sobrecargados": 0, "por_fase": {},
            "por_persona": [],
        }

    total_estimadas = sum(r["horas_estimadas"] or 0 for r in recursos)
    total_reales = sum(r["horas_reales"] or 0 for r in recursos)

    por_persona = defaultdict(lambda: {"estimadas": 0, "reales": 0, "capacidad": 40})
    for r in recursos:
        persona = r["persona"] or "Sin asignar"
        por_persona[persona]["estimadas"] += r["horas_estimadas"] or 0
        por_persona[persona]["reales"] += r["horas_reales"] or 0
        por_persona[persona]["capacidad"] = r["capacidad_semanal"] or 40

    personas_lista = []
    sobrecargados = 0
    for persona, datos in por_persona.items():
        estimadas = datos["estimadas"]
        reales = datos["reales"]
        capacidad = datos["capacidad"]
        semanas = reales / HH_DIARIAS / 5 if reales else 0
        utilizacion = (reales / (capacidad * semanas) * 100) if semanas > 0 else 0

        if utilizacion > 100:
            sobrecargados += 1

        personas_lista.append({
            "persona": persona,
            "horas_estimadas": estimadas,
            "horas_reales": reales,
            "capacidad_semanal": capacidad,
            "utilizacion": round(utilizacion, 1),
        })

    por_fase = defaultdict(int)
    for r in recursos:
        fase = r["fase_actual"] or "Sin fase"
        por_fase[fase] += 1

    return {
        "total": total,
        "total_horas_estimadas": total_estimadas,
        "total_horas_reales": total_reales,
        "promedio_utilizacion": round(sum(p["utilizacion"] for p in personas_lista) / len(personas_lista), 1) if personas_lista else 0,
        "sobrecargados": sobrecargados,
        "por_fase": dict(por_fase),
        "por_persona": sorted(personas_lista, key=lambda x: x["utilizacion"], reverse=True),
    }


def _aplicar_estilo(celda, font=None, fill=None, alignment=None, border=None):
    if font:
        celda.font = font
    if fill:
        celda.fill = fill
    if alignment:
        celda.alignment = alignment
    if border:
        celda.border = border


def _merge_y_escribir(ws, r1, c1, r2, c2, valor, font, alignment=None, fill=None):
    ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)
    celda = ws.cell(r1, c1, valor)
    _aplicar_estilo(celda, font=font, alignment=alignment or Alignment(horizontal="left"), fill=fill)


def _obtener_fill_utilizacion(utilizacion):
    """Retorna fill según la utilización."""
    if utilizacion > 100:
        return FILL_SOBRECARGA
    elif utilizacion > 80:
        return FILL_ALTA
    elif utilizacion > 50:
        return FILL_MEDIA
    else:
        return FILL_BAJA


def agregar_hoja_recursos(wb, recursos, metricas, fecha_gen):
    """Agrega la hoja de análisis de recursos al workbook."""
    ws = wb.create_sheet("Análisis de Recursos")
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 15
    ws.column_dimensions["C"].width = 15
    ws.column_dimensions["D"].width = 15
    ws.column_dimensions["E"].width = 15
    ws.column_dimensions["F"].width = 15
    ws.column_dimensions["G"].width = 15

    # Título
    _merge_y_escribir(ws, 1, 1, 1, 7, "ANÁLISIS DE RECURSOS", FONT_TITULO, ALIGN_CENTER)
    _merge_y_escribir(ws, 2, 1, 2, 7, f"Fecha: {fecha_gen}", Font(name="Calibri", size=10, color="FF97999B"), ALIGN_CENTER)

    # Resumen
    row = 4
    _merge_y_escribir(ws, row, 1, row, 7, "RESUMEN", FONT_SECCION)
    row += 1
    headers_resumen = ["Total Personas", "Horas Estimadas", "Horas Reales", "Utilización Promedio", "Sobrecargados"]
    for c, h in enumerate(headers_resumen, 1):
        celda = ws.cell(row, c, h)
        _aplicar_estilo(celda, font=FONT_HEADER, fill=FILL_HEADER, border=THIN_BORDER)
    row += 1
    valores = [metricas["total"], metricas["total_horas_estimadas"], metricas["total_horas_reales"],
               f"{metricas['promedio_utilizacion']}%", metricas["sobrecargados"]]
    for c, v in enumerate(valores, 1):
        celda = ws.cell(row, c, v)
        _aplicar_estilo(celda, font=FONT_BODY, border=THIN_BORDER, alignment=ALIGN_CENTER)

    # Distribución por fase
    row += 2
    _merge_y_escribir(ws, row, 1, row, 7, "DISTRIBUCIÓN POR FASE", FONT_SECCION)
    row += 1
    for c, h in enumerate(["Fase", "Cantidad"], 1):
        celda = ws.cell(row, c, h)
        _aplicar_estilo(celda, font=FONT_HEADER, fill=FILL_HEADER, border=THIN_BORDER)
    row += 1
    for fase in FASES_RECURSO:
        cant = metricas["por_fase"].get(fase, 0)
        fill = FASES_FILL_MAP.get(fase)
        for c, v in enumerate([fase, cant], 1):
            celda = ws.cell(row, c, v)
            _aplicar_estilo(celda, font=FONT_BODY, border=THIN_BORDER, fill=fill,
                           alignment=ALIGN_CENTER if c > 1 else None)
        row += 1

    # Detalle por persona
    row += 1
    _merge_y_escribir(ws, row, 1, row, 7, "DETALLE POR PERSONA", FONT_SECCION)
    row += 1
    headers = ["Persona", "Horas Estimadas", "Horas Reales", "Capacidad Semanal", "Utilización", "Estado", "Fase"]
    for c, h in enumerate(headers, 1):
        celda = ws.cell(row, c, h)
        _aplicar_estilo(celda, font=FONT_HEADER, fill=FILL_HEADER, border=THIN_BORDER)
    row += 1

    for p in metricas["por_persona"]:
        fill_util = _obtener_fill_utilizacion(p["utilizacion"])
        estado = "Sobrecargado" if p["utilizacion"] > 100 else ("Alta" if p["utilizacion"] > 80 else "Normal")
        vals = [p["persona"], p["horas_estimadas"], p["horas_reales"], p["capacidad_semanal"],
                f"{p['utilizacion']}%", estado, ""]
        for c, v in enumerate(vals, 1):
            celda = ws.cell(row, c, v)
            _aplicar_estilo(celda, font=FONT_BODY, border=THIN_BORDER, fill=fill_util,
                           alignment=ALIGN_CENTER if c > 1 else None)
        row += 1


def main():
    print("Leyendo recursos...")
    recursos = leer_recursos()

    if not recursos:
        print("No se encontraron recursos. Asegúrese de que la hoja 'Recursos' exista en el Excel.")
        return

    metricas = calcular_metricas(recursos)
    fecha_gen = datetime.now().strftime("%d/%m/%Y")

    print(f"  Total personas: {metricas['total']}")
    print(f"  Horas estimadas: {metricas['total_horas_estimadas']}")
    print(f"  Horas reales: {metricas['total_horas_reales']}")
    print(f"  Utilización promedio: {metricas['promedio_utilizacion']}%")
    print(f"  Sobrecargados: {metricas['sobrecargados']}")

    try:
        wb = openpyxl.load_workbook(ARCHIVO_SALIDA_REPORTE)
    except FileNotFoundError:
        print(f"Archivo de reporte no encontrado: {ARCHIVO_SALIDA_REPORTE}")
        print("Ejecute primero generar_reporte_nevasa.py")
        return

    agregar_hoja_recursos(wb, recursos, metricas, fecha_gen)

    archivo_temp = ARCHIVO_SALIDA_REPORTE.replace(".xlsx", "_temp.xlsx")
    wb.save(archivo_temp)
    try:
        os.replace(archivo_temp, ARCHIVO_SALIDA_REPORTE)
    except PermissionError:
        print(f"\n  [!] No se pudo sobrescribir. Guardado como: {archivo_temp}")
        return
    print(f"\nAnálisis de recursos agregado a: {ARCHIVO_SALIDA_REPORTE}")


if __name__ == "__main__":
    main()
