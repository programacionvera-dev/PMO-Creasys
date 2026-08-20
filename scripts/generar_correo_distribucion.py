"""
Generador de Correo de Distribución
Genera template HTML para notificar al PM sobre nuevos requerimientos para distribución.

Uso:
    python scripts/generar_correo_distribucion.py
    python scripts/generar_correo_distribucion.py --requerimientos 5 --criticos 2
"""
import sys
import os
import argparse
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.rutas import (
    CARPETA_SALIDA_TEMPLATES, URL_FIRMA,
    ARCHIVO_SEGUIMIENTO,
    MAPEO_SEGUI, MAPEO_REQUERIMIENTO, MAPEO_ESTADO,
    MAPEO_AREA, MAPEO_ETAPA, MAPEO_TIPO, MAPEO_DETALLE
)

try:
    from config.cliente_actual import cliente
    CLIENTE_NOMBRE = cliente["nombre"]
except ImportError:
    CLIENTE_NOMBRE = "Nevasa"


def contar_nuevos_pendientes():
    """Cuenta requerimientos nuevos pendientes de distribución."""
    try:
        df = pd.read_excel(ARCHIVO_SEGUIMIENTO, sheet_name=MAPEO_SEGUI["hoja"], engine="openpyxl")
        
        # Filtrar por estados pendientes de distribución
        estados_pendientes = ["Sin Formalizar", "Pendiente"]
        pendientes = df[df[MAPEO_ESTADO].astype(str).str.upper().isin([e.upper() for e in estadospendientes])]
        
        total = len(pendientes)
        criticos = len(pendientes[pendientes[MAPEO_AREA].astype(str).str.upper() == "INCIDENCIA"])
        mejoras = len(pendientes[pendientes[MAPEO_AREA].astype(str).str.upper() == "MEJORA"])
        evolutivos = len(pendientes[pendientes[MAPEO_AREA].astype(str).str.upper() == "EVOLUTIVO"])
        
        return {
            "total": total,
            "criticos": criticos,
            "mejoras": mejoras,
            "evolutivos": evolutivos
        }
    except Exception as e:
        return {"total": 0, "criticos": 0, "mejoras": 0, "evolutivos": 0, "error": str(e)}


def generar_correo_distribucion(stats=None):
    """Genera HTML para correo de distribución al PM."""
    if stats is None:
        stats = contar_nuevos_pendientes()
    
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Determinar prioridad basada en contenido
    prioridad_html = ""
    if stats.get("criticos", 0) > 0:
        prioridad_html = f"""
    <div style="background:#ffcccc;padding:15px;border-left:4px solid #cc0000;margin:20px 0">
        <h3 style="margin-top:0;color:#cc0000">&#x26A0; CRÍTICO: {stats.get('criticos', 0)} Incidencia(s) Pendiente(s)</h3>
        <p style="margin:0">Existen incidencias pendientes de distribución que requieren atención inmediata.</p>
    </div>"""
    
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Calibri,sans-serif;margin:20px;color:#333f48">
    <h2 style="color:#333f48;font-size:20px">&#x1F4E7; Notificación de Distribución de Requerimientos</h2>
    <p>Estimado PM,</p>
    <p>Se ha(n) detectado nuevo(s) requerimiento(s) pendiente(s) de distribución al equipo de desarrollo.</p>
    
    {prioridad_html}
    
    <div style="background:#f5f5f5;padding:15px;border-left:4px solid #2F5496;margin:20px 0">
        <h3 style="margin-top:0;color:#333f48">Resumen Pendiente</h3>
        <table style="border-collapse:collapse;width:100%;margin:10px 0">
            <tr>
                <td style="padding:5px 15px 5px 0"><strong>Total Pendientes:</strong></td>
                <td style="padding:5px 0">{stats.get('total', 0)}</td>
            </tr>
            <tr>
                <td style="padding:5px 15px 5px 0"><strong>Incidencias:</strong></td>
                <td style="padding:5px 0">{stats.get('criticos', 0)}</td>
            </tr>
            <tr>
                <td style="padding:5px 15px 5px 0"><strong>Mejoras:</strong></td>
                <td style="padding:5px 0">{stats.get('mejoras', 0)}</td>
            </tr>
            <tr>
                <td style="padding:5px 15px 5px 0"><strong>Evolutivos:</strong></td>
                <td style="padding:5px 0">{stats.get('evolutivos', 0)}</td>
            </tr>
        </table>
    </div>
    
    <div style="background:#f5f5f5;padding:15px;border-left:4px solid #fa4616;margin:20px 0">
        <h3 style="margin-top:0;color:#333f48">Acciones Requeridas</h3>
        <ol>
            <li>Revisar los requerimientos pendientes en <strong>Seguimiento Requerimientos {CLIENTE_NOMBRE}CB.xlsx</strong></li>
            <li>Asignar desarrollador responsable para cada uno</li>
            <li>Actualizar etapa de <strong>Sin Formalizar</strong> a <strong>En Desarrollo</strong></li>
            <li>Comunicar al equipo en la daily</li>
        </ol>
    </div>
    
    <div style="margin-top:30px;border-top:1px solid #97999B;padding-top:10px">
        <img src="{URL_FIRMA}" alt="Creasys" style="height:250px">
    </div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generador de correo de distribución")
    parser.add_argument("--requerimientos", type=int, help="Número total de requerimientos")
    parser.add_argument("--criticos", type=int, help="Número de incidencias")
    parser.add_argument("--mejoras", type=int, help="Número de mejoras")
    parser.add_argument("--evolutivos", type=int, help="Número de evolutivos")
    parser.add_argument("--output", "-o", help="Archivo de salida")
    
    args = parser.parse_args()
    
    # Usar argumentos o contar del Excel
    if args.requerimientos is not None:
        stats = {
            "total": args.requerimientos,
            "criticos": args.criticos or 0,
            "mejoras": args.mejoras or 0,
            "evolutivos": args.evolutivos or 0
        }
    else:
        stats = contar_nuevos_pendientes()
        if "error" in stats:
            print(f"Error leyendo Excel: {stats['error']}")
            print("Usando valores por defecto...")
            stats = {"total": 0, "criticos": 0, "mejoras": 0, "evolutivos": 0}
    
    html = generar_correo_distribucion(stats)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"HTML generado: {args.output}")
    else:
        os.makedirs(CARPETA_SALIDA_TEMPLATES, exist_ok=True)
        ruta = os.path.join(CARPETA_SALIDA_TEMPLATES, "correo_distribucion.html")
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"HTML generado: {ruta}")
        print(f"\nResumen: {stats.get('total', 0)} requerimientos pendientes")


if __name__ == "__main__":
    main()
