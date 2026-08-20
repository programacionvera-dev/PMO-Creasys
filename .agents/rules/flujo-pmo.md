# Reglas de Flujo de Trabajo PMO

## Contexto

Sistema GPI CB para el mercado financiero (Nevasa). Proyecto en Producción con 4 frentes de trabajo activos.

## Frentes de Trabajo

| # | Frente | Tipo Azure DevOps | Prioridad |
|---|--------|-------------------|-----------|
| 1 | Incidencias | Bug | #1 - Máxima |
| 2 | Mejoras | Product Backlog Item | #2 |
| 3 | Evolutivos | Feature | #3 |
| 4 | Backlog | Task | #4 |

## Regla Fundamental

> **Las incidencias siempre tienen prioridad sobre cualquier otro requerimiento.**

## Flujo por Frente

### Incidencias
```
Recepción → Diagnóstico → Desarrollo → QA → Producción → Cierre
```

### Mejoras
```
Solicitud → Análisis → Estimación → Aprobación → Desarrollo → QA → Producción → Cierre
```

### Evolutivos
```
Solicitud → Análisis → Estimación → Planificación → Desarrollo → QA → Producción → Cierre
```

### Backlog
```
Identificación → Priorización → Estimación → Sprint Planning → Desarrollo → Cierre
```

## Calendario de Reuniones

| Reunión | Frecuencia | Día/Hora |
|---------|------------|----------|
| Daily Dev | Diaria | Avance + Blockers + Prioridades |
| Cliente Nevasa | Semanal | Martes 16:00 |
| Reporte de estatus | 2x/semana | Lunes y Jueves (mismo formato) |

### Daily con Equipo Dev
- **Frecuencia:** Diaria
- **Duración:** 15-20 minutos
- **Temas:** Avance, Blockers, Prioridades, Compromisos

### Reunión con Cliente (Martes 16:00)
- **Duración:** 30-45 minutos
- **Agenda:** Incidencias → Mejoras → Evolutivos → Backlog → Próximos pasos

### Envío de Reportes
- **Días:** Lunes y Jueves
- **Mismo formato** para ambos días
- **Contenido:** Resumen ejecutivo, incidencias, mejoras, evolutivos, backlog

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

### Flujo Futuro

| # | Flujo | Trigger | Estado |
|---|---|---|---|
| 5 | Azure DevOps | Manual/API | 🔮 Futuro |

### Dependencias

```
Python (scripts)
├─ generar_plantillascorreo.py → HTMLs para flujos 1, 2, 3
└─ generar_reporte_nevasa.py → Excel para flujo 3

Power Automate
├─ Flujo 1 → Usa HTML de Python
├─ Flujo 2 → Usa HTML de Python
├─ Flujo 3 → Usa HTML + Excel de Python
└─ Flujo 4 → Independiente (genera Excel)

OneDrive
├─ plantillas_correo/ → HTMLs generados por Python
├─ Reporte_Estatus_GPI_CB.xlsx → Reporte generado por Python
└─ Seguimiento Requerimientos NevasaCB.xlsx → Excel fuente
```

## Integración Azure DevOps

### Áreas
```
GPI CB
├── Incidencias
├── Evolutivos
├── Mejoras
└── Backlog
```

### Tags Recomendados
- `Urgente` - Incidencias críticas
- `Cliente:Nevasa` - Filtrar por cliente
- `Sprint:Actual` - Tracking por sprint
- `Estado:Producción` - Desplegado

## Comunicación Cliente

| Tipo | Frecuencia | Canal |
|------|------------|-------|
| Reporte de estatus | Lunes y Jueves | Email (Power Automate) |
| Reunión avance | Martes 16:00 | Presencial/Teams |
| Incidencia crítica | Inmediata | Email + Llamada |
| Recepción automática | Cada correo | Power Automate |

## Métricas por Frente

| Frente | Métrica |
|--------|---------|
| Incidencias | Tiempo promedio resolución |
| Incidencias | % Resueltas en SLA |
| Mejoras | Lead time |
| Evolutivos | Velocidad (Story Points/Sprint) |
| Backlog | % Completado |
