"""
Generador de Seguimiento Diario
Genera resumen diario de avance para la daily con el equipo de desarrollo.

Uso:
    python scripts/generar_seguimiento_diario.py
    python scripts/generar_seguimiento_diario.py --output reporte.md
"""
import sys
import os
import argparse
import pandas as pd
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.rutas import (
    ARCHIVO_SEGUIMIENTO,
    MAPEO_SEGUI, MAPEO_SECUENCIAL, MAPEO_REQUERIMIENTO, MAPEO_DETALLE,
    MAPEO_AREA, MAPEO_ESTADO, MAPEO_ETAPA, MAPEO_PRIORIDAD,
    MAPEO_SOLICITANTE, MAPEO_FECHA_AVANCE, MAPEO_FECHA_INICIO, MAPEO_FECHA_CIERRE,
    MAPEO_TIPO, MAPEO_VERSION, MAPEO_MOTIVO
)

try:
    from config.cliente_actual import cliente
    CLIENTE_NOMBRE = cliente["nombre"]
except ImportError:
    CLIENTE_NOMBRE = "Nevasa"


def cargar_datos():
    """Carga los datos del Excel de seguimiento."""
    try:
        df = pd.read_excel(ARCHIVO_SEGUIMIENTO, sheet_name=MAPEO_SEGUI["hoja"], engine="openpyxl")
        return df
    except Exception as e:
        print(f"Error al cargar Excel: {e}")
        return None


def calcular_estadisticas(df):
    """Calcula estadísticas generales del proyecto."""
    stats = {}
    
    # Total de requerimientos
    stats["total"] = len(df)
    
    # Por área
    stats["incidencias"] = len(df[df[MAPEO_AREA].astype(str).str.upper() == "INCIDENCIA"])
    stats["mejoras"] = len(df[df[MAPEO_AREA].astype(str).str.upper() == "MEJORA"])
    stats["evolutivos"] = len(df[df[MAPEO_AREA].astype(str).str.upper() == "EVOLUTIVO"])
    
    # Por estado
    stats["pendientes"] = len(df[df[MAPEO_ESTADO].astype(str).str.upper().isin(["PENDIENTE", "SIN FORMALIZAR"])])
    stats["en_desarrollo"] = len(df[df[MAPEO_ESTADO].astype(str).str.upper() == "EN DESARROLLO"])
    stats["certificacion"] = len(df[df[MAPEO_ESTADO].astype(str).str.upper().isin(["CERTIFICACION", "CERTIFICACIÓN"])])
    stats["produccion"] = len(df[df[MAPEO_ESTADO].astype(str).str.upper() == "PRODUCCIÓN"])
    
    # Por prioridad
    stats["maxima"] = len(df[df[MAPEO_PRIORIDAD].astype(str).str.upper() == "MÁXIMA"])
    stats["alta"] = len(df[df[MAPEO_PRIORIDAD].astype(str).str.upper() == "ALTA"])
    stats["media"] = len(df[df[MAPEO_PRIORIDAD].astype(str).str.upper() == "MEDIA"])
    stats["baja"] = len(df[df[MAPEO_PRIORIDAD].astype(str).str.upper() == "BAJA"])
    
    # Avances recientes (última semana)
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)
    
    try:
        df[MAPEO_FECHA_AVANCE] = pd.to_datetime(df[MAPEO_FECHA_AVANCE], errors='coerce')
        recientes = df[df[MAPEO_FECHA_AVANCE] >= hace_7_dias]
        stats["avances_semana"] = len(recientes)
    except:
        stats["avances_semana"] = 0
    
    return stats


def obtener_avances_recientes(df, dias=7):
    """Obtiene los avances de los últimos días."""
    hoy = datetime.now()
    hace_dias = hoy - timedelta(days=dias)
    
    try:
        df[MAPEO_FECHA_AVANCE] = pd.to_datetime(df[MAPEO_FECHA_AVANCE], errors='coerce')
        recientes = df[df[MAPEO_FECHA_AVANCE] >= hace_dias].copy()
        recientes = recientes.sort_values(MAPEO_FECHA_AVANCE, ascending=False)
        return recientes
    except:
        return pd.DataFrame()


def obtener_criticos(df):
    """Obtiene los requerimientos críticos pendientes."""
    criticos = df[
        (df[MAPEO_PRIORIDAD].astype(str).str.upper().isin(["MÁXIMA", "ALTA"])) &
        (df[MAPEO_ESTADO].astype(str).str.upper().isin(["PENDIENTE", "SIN FORMALIZAR", "EN DESARROLLO"]))
    ].copy()
    return criticos


def generar_reporte_markdown(stats, avances, criticos):
    """Genera reporte en formato Markdown."""
    fecha = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M")
    
    md = f"""# Reporte Diario - {CLIENTE_NOMBRE}
**Fecha:** {fecha} | **Hora:** {hora}

---

## Resumen General

| Métrica | Valor |
|---------|-------|
| Total Requerimientos | {stats['total']} |
| Incidencias | {stats['incidencias']} |
| Mejoras | {stats['mejoras']} |
| Evolutivos | {stats['evolutivos']} |

## Estado Actual

| Estado | Cantidad |
|--------|----------|
| Pendientes | {stats['pendientes']} |
| En Desarrollo | {stats['en_desarrollo']} |
| Certificación | {stats['certificacion']} |
| Producción | {stats['produccion']} |

## Por Prioridad

| Prioridad | Cantidad |
|-----------|----------|
| Máxima | {stats['maxima']} |
| Alta | {stats['alta']} |
| Media | {stats['media']} |
| Baja | {stats['baja']} |

---

## Avances Últimos 7 Días

**Total avances:** {stats['avances_semana']}

"""
    
    if not avances.empty:
        md += "| ID | Requerimiento | Área | Estado | Último Avance |\n"
        md += "|----|---------------|------|--------|----------------|\n"
        for _, row in avances.head(10).iterrows():
            id_val = row.get(MAPEO_SECUENCIAL, "N/A")
            req_val = str(row.get(MAPEO_REQUERIMIENTO, "N/A"))[:50]
            area_val = row.get(MAPEO_AREA, "N/A")
            estado_val = row.get(MAPEO_ESTADO, "N/A")
            avance_val = row.get(MAPEO_FECHA_AVANCE, "N/A")
            if pd.notna(avance_val):
                avance_val = avance_val.strftime("%d/%m")
            md += f"| {id_val} | {req_val} | {area_val} | {estado_val} | {avance_val} |\n"
    else:
        md += "_No hay avances registrados en la última semana._\n"
    
    md += f"""
---

## Requerimientos Críticos Pendientes

"""
    
    if not criticos.empty:
        md += "| ID | Requerimiento | Área | Prioridad | Estado |\n"
        md += "|----|---------------|------|-----------|--------|\n"
        for _, row in criticos.head(10).iterrows():
            id_val = row.get(MAPEO_SECUENCIAL, "N/A")
            req_val = str(row.get(MAPEO_REQUERIMIENTO, "N/A"))[:50]
            area_val = row.get(MAPEO_AREA, "N/A")
            prioridad_val = row.get(MAPEO_PRIORIDAD, "N/A")
            estado_val = row.get(MAPEO_ESTADO, "N/A")
            md += f"| {id_val} | {req_val} | {area_val} | {prioridad_val} | {estado_val} |\n"
    else:
        md += "_No hay requerimientos críticos pendientes._\n"
    
    md += f"""
---

## Próximos Pasos

1. Revisar avances del día
2. Identificar blockers
3. Asignar prioridades
4. Compromisos del equipo

---
_Reporte generado automáticamente - {CLIENTE_NOMBRE} PMO_
"""
    
    return md


def generar_texto_plano(stats):
    """Genera resumen en texto plano para la daily."""
    fecha = datetime.now().strftime("%d/%m/%Y")
    
    texto = f"""
=== RESUMEN DIARIO {CLIENTE_NOMBRE} - {fecha} ===

TOTAL: {stats['total']} requerimientos
├─ Incidencias: {stats['incidencias']}
├─ Mejoras: {stats['mejoras']}
└─ Evolutivos: {stats['evolutivos']}

ESTADO:
├─ Pendientes: {stats['pendientes']}
├─ En Desarrollo: {stats['en_desarrollo']}
├─ Certificación: {stats['certificacion']}
└─ Producción: {stats['produccion']}

PRIORIDAD:
├─ Máxima: {stats['maxima']}
├─ Alta: {stats['alta']}
├─ Media: {stats['media']}
└─ Baja: {stats['baja']}

AVANCES SEMANA: {stats['avances_semana']}

============================================
"""
    return texto


def main():
    parser = argparse.ArgumentParser(description="Generador de seguimiento diario")
    parser.add_argument("--output", "-o", help="Archivo de salida")
    parser.add_argument("--texto", action="store_true", help="Generar texto plano en lugar de Markdown")
    parser.add_argument("--dias", type=int, default=7, help="Días para avances recientes")
    
    args = parser.parse_args()
    
    # Cargar datos
    df = cargar_datos()
    if df is None:
        print("No se pudo cargar el archivo de seguimiento")
        return
    
    # Calcular estadísticas
    stats = calcular_estadisticas(df)
    
    if args.texto:
        # Generar texto plano
        texto = generar_texto_plano(stats)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(texto)
            print(f"Texto generado: {args.output}")
        else:
            print(texto)
    else:
        # Generar reporte Markdown
        avances = obtener_avances_recientes(df, args.dias)
        criticos = obtener_criticos(df)
        md = generar_reporte_markdown(stats, avances, criticos)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"Reporte generado: {args.output}")
        else:
            # Guardar por defecto
            os.makedirs("reportes", exist_ok=True)
            fecha = datetime.now().strftime("%Y%m%d")
            ruta = os.path.join("reportes", f"seguimiento_diario_{fecha}.md")
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"Reporte generado: {ruta}")
            print("\n--- VISTA PREVIA ---")
            print(md[:1000] + "...")


if __name__ == "__main__":
    main()
