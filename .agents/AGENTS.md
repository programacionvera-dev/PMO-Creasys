# Agentes PMO Creasys

Repositorio de scripts y herramientas para la gestión de proyectos PMO.

Soporte multi-cliente mediante configuración JSON.

## Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `generar_reporte_nevasa.py` | Genera reporte ejecutivo en Excel (incluye riesgos, lessons, recursos) |
| `generar_plantillascorreo.py` | Genera plantillas HTML para correos |
| `generar_datos_powerbi.py` | Genera datos pre-calculados para Power BI |
| `generar_riesgos.py` | Genera análisis de riesgos |
| `generar_lessons_learned.py` | Genera reporte de lessons learned |
| `generar_recursos.py` | Genera análisis de asignación de recursos |
| `generar_correo_recepcion.py` | Genera template de correo para registro manual de requerimientos |
| `generar_correo_distribucion.py` | Genera correo de notificación para distribución de requerimientos |
| `generar_seguimiento_diario.py` | Genera resumen diario de avance para daily |

## Configuración Multi-Cliente

### Seleccionar Cliente

```bash
# Usar Nevasa (default)
python scripts/generar_reporte_nevasa.py

# Usar otro cliente
set PMO_CLIENTE=otro_cliente
python scripts/generar_reporte_nevasa.py
```

### Estructura de Configuración

```
scripts/config/
├── rutas.py                    # Rutas genéricas (lee config del cliente)
├── cliente_actual.py           # Helper para cargar config
└── clientes/
    ├── nevasa.json             # Config Nevasa
    └── template_cliente.json   # Template para nuevos clientes
```

### Agregar Nuevo Cliente

1. Copiar `template_cliente.json` como `nuevo_cliente.json`
2. Modificar rutas, mapeo de columnas, estados, branding
3. Crear hojas en Excel: Riesgos, Lessons Learned, Recursos
4. Ejecutar scripts con `set PMO_CLIENTE=nuevo_cliente`

## Módulos PMO

### Risk Management
- **Hoja Excel**: "Riesgos"
- **Script**: `generar_riesgos.py`
- **Documentación**: `docs/REGLAS_RIESGOS.md`

### Lessons Learned
- **Hoja Excel**: "Lessons Learned"
- **Script**: `generar_lessons_learned.py`
- **Documentación**: `docs/REGLAS_LESSONS_LEARNED.md`

### Resource Allocation
- **Hoja Excel**: "Recursos"
- **Script**: `generar_recursos.py`
- **Documentación**: `docs/REGLAS_RECURSOS.md`

## Flujos Power Automate

### Flujos Activos

| # | Flujo | Trigger | Estado |
|---|---|---|---|
| 1 | Certificación QA | Martes 9AM | ✅ Activo |
| 2 | Producción | Configurar | ✅ Activo |
| 3 | Estatus Cliente | Lunes/Jueves | ✅ Activo |

### Flujo Pendiente

| # | Flujo | Trigger | Estado |
|---|---|---|---|
| 4 | Recepción Automática | Correo entrante | ⏸ Pendiente |

Documentación completa: `docs/FLUJOS_POWER_AUTOMATE.md`

## Documentación

| Archivo | Contenido |
|---------|-----------|
| `docs/REGLAS_REPORTE.md` | Reglas del reporte ejecutivo |
| `docs/REGLAS_RIESGOS.md` | Reglas del módulo de riesgos |
| `docs/REGLAS_LESSONS_LEARNED.md` | Reglas de lessons learned |
| `docs/REGLAS_RECURSOS.md` | Reglas de recursos |
| `docs/FLUJO_TRABAJO_PMO.md` | Flujo de trabajo para 4 frentes |
| `docs/CONFIGURACION_POWER_AUTOMATE.md` | Configuración Power Automate |
| `docs/FLUJOS_POWER_AUTOMATE.md` | Documentación completa de flujos |
| `docs/Guia_PowerBI_Nevasa.md` | Guía de Power BI |

## Reglas del Agente

| Archivo | Contenido |
|---------|-----------|
| `.agents/rules/nevasa-pmo.md` | Reglas específicas Nevasa |
| `.agents/rules/riesgos-pmo.md` | Reglas de riesgos |
| `.agents/rules/lessons-learned-pmo.md` | Reglas de lessons learned |
| `.agents/rules/recursos-pmo.md` | Reglas de recursos |
| `.agents/rules/flujo-pmo.md` | Reglas del flujo de trabajo |
| `.agents/skills/project-manager/SKILL.md` | Skill de gestión de proyectos |

## Flujo de Trabajo

### Frentes de Trabajo

| # | Frente | Prioridad |
|---|--------|-----------|
| 1 | Incidencias | #1 - Máxima |
| 2 | Mejoras | #2 |
| 3 | Evolutivos | #3 |
| 4 | Backlog | #4 |

> **Regla**: Las incidencias siempre tienen prioridad sobre cualquier otro requerimiento.

### Calendario de Reuniones

| Reunión | Frecuencia | Día/Hora |
|---------|------------|----------|
| Daily Dev | Diaria | Avance + Blockers + Prioridades |
| Cliente Nevasa | Semanal | Martes 16:00 |
| Reporte de estatus | 2x/semana | Lunes y Jueves (mismo formato) |

### Checklist Semanal

| Día | Actividad |
|---|---|
| Lunes | Envío reporte de estatus |
| Martes | Daily + Reunión cliente (16:00) |
| Miércoles | Daily |
| Jueves | Envío reporte de estatus |
| Viernes | Daily + Cierre de semana |

Ver `docs/FLUJO_TRABAJO_PMO.md` para detalles completos.
