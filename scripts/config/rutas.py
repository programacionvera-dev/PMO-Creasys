"""
Configuracion de rutas para el proyecto Nevasa PMO.

Las rutas de entrada y salida apuntan a OneDrive para acceso del equipo.
Los scripts en este repositorio leen de OneDrive y generan en OneDrive.
"""
import os

# Directorio base del repositorio (PMO-Creasys)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Directorio de salida (OneDrive - CREASYS)
OUTPUT_DIR = os.path.join(
    os.environ.get("USERPROFILE", ""),
    "OneDrive - CREASYS S.A",
    "Gesti\u00f3n Nevasa"
)

# Directorio de gestion y revision
GESTION_DIR = os.path.join(OUTPUT_DIR, "Gesti\u00f3n y Revisi\u00f3n")

# ==================== ARCHIVOS DE ENTRADA ====================
ARCHIVO_FUENTE = os.path.join(GESTION_DIR, "Seguimiento Requerimientos NevasaCB.xlsx")

# ==================== ARCHIVOS DE SALIDA ====================
# Reporte de estatus
ARCHIVO_SALIDA_REPORTE = os.path.join(GESTION_DIR, "Reporte_Estatus_GPI_CB.xlsx")

# Datos para Power BI
ARCHIVO_SALIDA_POWERBI = os.path.join(GESTION_DIR, "Datos_PowerBI_Nevasa.xlsx")

# Templates de correo
CARPETA_SALIDA_TEMPLATES = os.path.join(GESTION_DIR, "plantillas_correo")

# ==================== ARCHIVOS DE PLANTILLA ====================
# Templates base (en el repositorio)
PLANTILLAS_DIR = os.path.join(BASE_DIR, "templates")
PLANTILLA_REPORTE_BASE = os.path.join(PLANTILLAS_DIR, "base", "reporte_estatus.html")

# Assets (en el repositorio)
ASSETS_DIR = os.path.join(PLANTILLAS_DIR, "assets")
URL_FIRMA = "https://www.creasys.cl/imagenes/firmas/Firma_Soporte-GPI-520x200.png"

# ==================== CONFIGURACION ====================
HH_DIARIAS = 8
PORCENTAJE_MARCA = 0.25
