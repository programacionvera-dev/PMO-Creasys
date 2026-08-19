# PMO Creasys

Repositorio de scripts y herramientas para la gestión de proyectos PMO.

## Estructura

```
PMO-Creasys/
├── scripts/
│   ├── config/
│   │   └── rutas.py
│   ├── generar_reporte_nevasa.py
│   ├── generar_plantillascorreo.py
│   └── generar_datos_powerbi.py
├── templates/
│   ├── base/
│   │   └── reporte_estatus.html
│   └── assets/
│       └── Firma_creasys.png
├── office-scripts/
│   └── actualizar_aprobado_pap.ts
├── docs/
│   ├── REGLAS_REPORTE.md
│   ├── CONFIGURACION_POWER_AUTOMATE.md
│   └── Guia_PowerBI_Nevasa.md
└── .agents/
    ├── AGENTS.md
    └── rules/
        └── nevasa-pmo.md
```

## Instalación

```bash
pip install openpyxl
```

## Uso

```bash
# Generar reporte ejecutivo
python scripts/generar_reporte_nevasa.py

# Generar plantillas de correo
python scripts/generar_plantillascorreo.py

# Generar datos para Power BI
python scripts/generar_datos_powerbi.py
```

## Configuración

Las rutas están centralizadas en `scripts/config/rutas.py`.

## Documentación

Ver `docs/` para documentación detallada.
