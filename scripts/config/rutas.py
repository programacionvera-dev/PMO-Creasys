"""
Configuracion de rutas para el proyecto PMO Creasys.

Soporte multi-cliente: Lee configuracion desde JSON del cliente actual.
Variable de entorno PMO_CLIENTE para seleccionar cliente (default: nevasa).
"""
import os
import json

# Directorio base del repositorio (PMO-Creasys)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _obtener_cliente():
    """Obtiene el nombre del cliente desde variable de entorno o default."""
    return os.environ.get("PMO_CLIENTE", "nevasa").lower()


def _cargar_config_cliente(cliente_nombre):
    """Carga el archivo JSON de configuracion del cliente."""
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clientes")
    ruta_config = os.path.join(config_dir, f"{cliente_nombre}.json")

    if not os.path.exists(ruta_config):
        raise FileNotFoundError(
            f"Configuracion no encontrada para cliente '{cliente_nombre}'. "
            f"Archivo esperado: {ruta_config}"
        )

    with open(ruta_config, "r", encoding="utf-8") as f:
        return json.load(f)


# Cargar configuracion del cliente actual
_cliente_nombre = _obtener_cliente()
_cliente_config = _cargar_config_cliente(_cliente_nombre)

# ==================== DIRECTORIOS ====================
# Directorio de salida (OneDrive)
OUTPUT_DIR = os.path.join(
    os.environ.get("USERPROFILE", ""),
    "OneDrive - CREASYS S.A",
    _cliente_config["carpeta_onedrive"]
)

# Directorio de gestion y revision
GESTION_DIR = os.path.join(OUTPUT_DIR, _cliente_config["subcarpeta"])

# ==================== ARCHIVOS DE ENTRADA ====================
ARCHIVO_FUENTE = os.path.join(GESTION_DIR, _cliente_config["archivo_fuente"])

# ==================== ARCHIVOS DE SALIDA ====================
ARCHIVO_SALIDA_REPORTE = os.path.join(GESTION_DIR, _cliente_config["archivos_salida"]["reporte"])
ARCHIVO_SALIDA_POWERBI = os.path.join(GESTION_DIR, _cliente_config["archivos_salida"]["powerbi"])
CARPETA_SALIDA_TEMPLATES = os.path.join(GESTION_DIR, _cliente_config["archivos_salida"]["templates"])

# ==================== ARCHIVOS DE PLANTILLA ====================
PLANTILLAS_DIR = os.path.join(BASE_DIR, "templates")
PLANTILLA_REPORTE_BASE = os.path.join(PLANTILLAS_DIR, "base", "reporte_estatus.html")
ASSETS_DIR = os.path.join(PLANTILLAS_DIR, "assets")
URL_FIRMA = _cliente_config["url_firma"]

# ==================== CONFIGURACION ====================
HH_DIARIAS = _cliente_config["configuracion"]["hh_diarias"]
PORCENTAJE_MARCA = _cliente_config["configuracion"]["porcentaje_marca"]

# ==================== MAPEO DE COLUMNAS ====================
MAPEO_COLUMNAS = _cliente_config["mapeo_columnas"]
MAPEO_RIESGOS = _cliente_config["mapeo_columnas_riesgos"]
MAPEO_LESSONS = _cliente_config["mapeo_columnas_lessons"]
MAPEO_RECURSOS = _cliente_config["mapeo_columnas_recursos"]

# ==================== ESTADOS Y CATEGORIAS ====================
ESTADOS = _cliente_config["estados"]
ESTADOS_RIESGO = _cliente_config["estados_riesgo"]
CATEGORIAS_LESSON = _cliente_config["categorias_lesson"]
FASES_RECURSO = _cliente_config["fases_recurso"]
PRIORIDADES = _cliente_config["prioridades"]

# ==================== BRANDING ====================
BRANDING = _cliente_config["branding"]
COLOR_PRIMARIO = BRANDING["color_primario"]
COLOR_SECUNDARIO = BRANDING["color_secundario"]
NOMBRE_REPORTE = BRANDING["nombre_reporte"]

# ==================== UMBRALES DE RIESGO ====================
UMBRALES_RIESGO = _cliente_config["configuracion"]["umbrales_riesgo"]
