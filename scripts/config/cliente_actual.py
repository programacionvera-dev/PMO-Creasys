"""
Helper para cargar la configuración del cliente actual.

Uso:
    from config.cliente_actual import cliente, mapeo, estados, config
"""
import os
import json


def _obtener_cliente():
    """Obtiene el nombre del cliente desde variable de entorno o default."""
    return os.environ.get("PMO_CLIENTE", "nevasa").lower()


def _cargar_config(cliente_nombre):
    """Carga el archivo JSON de configuración del cliente."""
    config_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_config = os.path.join(config_dir, f"{cliente_nombre}.json")

    if not os.path.exists(ruta_config):
        raise FileNotFoundError(
            f"Configuración no encontrada para cliente '{cliente_nombre}'. "
            f"Archivo esperado: {ruta_config}"
        )

    with open(ruta_config, "r", encoding="utf-8") as f:
        return json.load(f)


# Cargar configuración al importar
_cliente_nombre = _obtener_cliente()
cliente = _cargar_config(_cliente_nombre)

# Accesos directos
nombre = cliente["nombre"]
mapeo = cliente["mapeo_columnas"]
mapeo_riesgos = cliente["mapeo_columnas_riesgos"]
mapeo_lessons = cliente["mapeo_columnas_lessons"]
mapeo_recursos = cliente["mapeo_columnas_recursos"]
estados = cliente["estados"]
estados_riesgo = cliente["estados_riesgo"]
categorias_lesson = cliente["categorias_lesson"]
fases_recurso = cliente["fases_recurso"]
prioridades = cliente["prioridades"]
branding = cliente["branding"]
config = cliente["configuracion"]
