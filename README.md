# PMO Creasys

Repositorio de scripts y herramientas para la gestión de proyectos PMO.

Soporte multi-cliente mediante configuración JSON.

## Estructura

```
PMO-Creasys/
├── scripts/
│   ├── config/
│   │   ├── rutas.py                    # Rutas genéricas
│   │   ├── cliente_actual.py           # Helper de configuración
│   │   └── clientes/
│   │       ├── nevasa.json             # Config Nevasa
│   │       └── template_cliente.json   # Template nuevos clientes
│   ├── generar_reporte_nevasa.py       # Reporte ejecutivo
│   ├── generar_plantillascorreo.py     # Plantillas correo
│   ├── generar_datos_powerbi.py        # Datos Power BI
│   ├── generar_riesgos.py              # Análisis de riesgos
│   ├── generar_lessons_learned.py      # Lessons learned
│   └── generar_recursos.py             # Análisis de recursos
├── templates/
│   ├── base/
│   │   └── reporte_estatus.html
│   └── assets/
│       └── Firma_creasys.png
├── office-scripts/
│   └── actualizar_aprobado_pap.ts
├── docs/
│   ├── REGLAS_REPORTE.md
│   ├── REGLAS_RIESGOS.md
│   ├── REGLAS_LESSONS_LEARNED.md
│   ├── REGLAS_RECURSOS.md
│   ├── CONFIGURACION_POWER_AUTOMATE.md
│   └── Guia_PowerBI_Nevasa.md
└── .agents/
    ├── AGENTS.md
    ├── rules/
    │   ├── nevasa-pmo.md
    │   ├── riesgos-pmo.md
    │   ├── lessons-learned-pmo.md
    │   └── recursos-pmo.md
    └── skills/
        └── project-manager/
            └── SKILL.md
```

## Instalación

```bash
pip install openpyxl
```

## Uso

```bash
# Generar reporte ejecutivo (incluye riesgos, lessons, recursos)
python scripts/generar_reporte_nevasa.py

# Generar plantillas de correo
python scripts/generar_plantillascorreo.py

# Generar datos para Power BI
python scripts/generar_datos_powerbi.py

# Generar módulos individuales
python scripts/generar_riesgos.py
python scripts/generar_lessons_learned.py
python scripts/generar_recursos.py
```

## Multi-Cliente

```bash
# Usar Nevasa (default)
python scripts/generar_reporte_nevasa.py

# Usar otro cliente
set PMO_CLIENTE=otro_cliente
python scripts/generar_reporte_nevasa.py
```

## Configuración

Las rutas están centralizadas en `scripts/config/rutas.py` y se cargan desde archivos JSON en `scripts/config/clientes/`.

Para agregar un nuevo cliente:
1. Copiar `template_cliente.json` como `nuevo_cliente.json`
2. Modificar rutas, mapeo de columnas, estados, branding
3. Crear hojas en Excel: Riesgos, Lessons Learned, Recursos

## Documentación

Ver `docs/` para documentación detallada.
