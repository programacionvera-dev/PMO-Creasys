"""
Generador de Correo de Recepción Manual
Genera template HTML para registrar un nuevo requerimiento/incidencia de forma manual.

Uso:
    python scripts/generar_correo_recepcion.py
    python scripts/generar_correo_recepcion.py --requerimiento "Descripción" --solicitante "Nombre"
"""
import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.rutas import CARPETA_SALIDA_TEMPLATES, URL_FIRMA

try:
    from config.cliente_actual import cliente
    CLIENTE_NOMBRE = cliente["nombre"]
except ImportError:
    CLIENTE_NOMBRE = "Nevasa"


def generar_correo_recepcion(requerimiento="", solicitante="", area="", prioridad=""):
    """Genera HTML para correo de registro manual de requerimiento."""
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Calibri,sans-serif;margin:20px;color:#333f48">
    <h2 style="color:#333f48;font-size:20px">&#x1F4CB; Registro de Nuevo Requerimiento</h2>
    <p>Estimados:</p>
    <p>Se ha recibido un nuevo requerimiento/incidencia que requiere ser registrado en el sistema de seguimiento.</p>
    
    <div style="background:#f5f5f5;padding:15px;border-left:4px solid #2F5496;margin:20px 0">
        <h3 style="margin-top:0;color:#333f48">Datos del Requerimiento</h3>
        <table style="border-collapse:collapse;width:100%;margin:10px 0">
            <tr>
                <td style="padding:5px 15px 5px 0"><strong>Fecha:</strong></td>
                <td style="padding:5px 0">{fecha}</td>
            </tr>
            <tr>
                <td style="padding:5px 15px 5px 0"><strong>Requerimiento:</strong></td>
                <td style="padding:5px 0">{requerimiento or '[Completar]'}</td>
            </tr>
            <tr>
                <td style="padding:5px 15px 5px 0"><strong>Solicitante:</strong></td>
                <td style="padding:5px 0">{solicitante or '[Completar]'}</td>
            </tr>
            <tr>
                <td style="padding:5px 15px 5px 0"><strong>Área:</strong></td>
                <td style="padding:5px 0">{area or '[Completar]'}</td>
            </tr>
            <tr>
                <td style="padding:5px 15px 5px 0"><strong>Prioridad:</strong></td>
                <td style="padding:5px 0">{prioridad or '[Completar]'}</td>
            </tr>
        </table>
    </div>
    
    <div style="background:#f5f5f5;padding:15px;border-left:4px solid #fa4616;margin:20px 0">
        <h3 style="margin-top:0;color:#333f48">Acciones Requeridas</h3>
        <ol>
            <li>Registrar este requerimiento en <strong>Seguimiento Requerimientos {CLIENTE_NOMBRE}CB.xlsx</strong></li>
            <li>Asignar número de índice consecutivo</li>
            <li>Establecer etapa: <strong>Sin Formalizar</strong></li>
            <li>Informar al PM para distribución al equipo</li>
        </ol>
    </div>

    <div style="background:#fff3cd;padding:15px;border-left:4px solid #ffc107;margin:20px 0">
        <p style="margin:0"><strong style="color:#856404">Nota:</strong> Si el flujo automatizado está activo, este paso se realiza automáticamente al recibir el correo en el buzón compartido.</p>
    </div>
    
    <div style="margin-top:30px;border-top:1px solid #97999B;padding-top:10px">
        <img src="{URL_FIRMA}" alt="Creasys" style="height:250px">
    </div>
</body>
</html>"""


def generar_correo_simple(requerimiento, solicitante, area="", prioridad=""):
    """Genera texto plano para copiar rápido."""
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    texto = f"""=== NUEVO REQUERIMIENTO {CLIENTE_NOMBRE} ===

Fecha: {fecha}
Requerimiento: {requerimiento}
Solicitante: {solicitante}
Área: {area or '[Pendiente]'}
Prioridad: {prioridad or '[Pendiente]'}

--- ACCIONES ---
1. Registrar en Seguimiento Requerimientos {CLIENTE_NOMBRE}CB.xlsx
2. Asignar índice consecutivo
3. Etapa: Sin Formalizar
4. Informar al PM

================================"""
    return texto


def main():
    parser = argparse.ArgumentParser(description="Generador de correo de recepción manual")
    parser.add_argument("--requerimiento", "-r", help="Descripción del requerimiento")
    parser.add_argument("--solicitante", "-s", help="Nombre del solicitante")
    parser.add_argument("--area", "-a", help="Área del solicitante")
    parser.add_argument("--prioridad", "-p", help="Prioridad (MÁXIMA, ALTA, MEDIA, BAJA)")
    parser.add_argument("--html", action="store_true", help="Generar HTML en lugar de texto")
    parser.add_argument("--output", "-o", help="Archivo de salida")
    
    args = parser.parse_args()
    
    if args.html or not args.requerimiento:
        # Generar HTML
        html = generar_correo_recepcion(
            requerimiento=args.requerimiento or "",
            solicitante=args.solicitante or "",
            area=args.area or "",
            prioridad=args.prioridad or ""
        )
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"HTML generado: {args.output}")
        else:
            # Guardar en carpeta de templates
            os.makedirs(CARPETA_SALIDA_TEMPLATES, exist_ok=True)
            ruta = os.path.join(CARPETA_SALIDA_TEMPLATES, "correo_recepcion.html")
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"HTML generado: {ruta}")
            print("\n--- VISTA PREVIA ---")
            print(html[:500] + "...")
    else:
        # Generar texto plano
        texto = generar_correo_simple(
            requerimiento=args.requerimiento,
            solicitante=args.solicitante or "",
            area=args.area or "",
            prioridad=args.prioridad or ""
        )
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(texto)
            print(f"Texto generado: {args.output}")
        else:
            print(texto)


if __name__ == "__main__":
    main()
