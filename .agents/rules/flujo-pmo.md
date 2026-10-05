# Reglas de Flujo de Trabajo PMO

## Contexto

Sistema GPI CB para el mercado financiero (Nevasa). Proyecto en Producción con 4 frentes de trabajo activos.

## Frentes de Trabajo

Basado en **PMBOK 7ª Edición** - Gestión de Entregas y **Azure DevOps Best Practices**:

| # | Frente | Tipo Azure DevOps | Prioridad PMBOK | Descripción |
|---|--------|-------------------|-----------------|-------------|
| 1 | Incidencias | Bug | #1 - Corregir | Defectos, bugs, problemas en producción |
| 2 | Evolutivos | Feature | #2 - Crear | Nuevas funcionalidades, valor nuevo al negocio |
| 3 | Mejoras | Product Backlog Item | #3 - Optimizar | Mejoras incrementales a funcionalidad existente |
| 4 | Backlog | Task | #4 - Planificar | Ideas, tareas pendientes de priorizar |

> **Referencia PMBOK:** Gestión de la Calidad - Los defectos (incidencias) tienen prioridad sobre nuevas funcionalidades para mantener la estabilidad del sistema en producción.

## Regla Fundamental

> **Las incidencias siempre tienen prioridad sobre cualquier otro requerimiento.**
> *Alineado con PMBOK: Gestión de Riesgos - Mitigar problemas críticos antes de agregar nueva funcionalidad.*

## Flujo por Frente

### Incidencias (Corregir)
```
Recepción → Diagnóstico → Desarrollo → QA → Producción → Cierre
```
> **PMBOK:** Ciclo de vida de corrección de defectos

### Evolutivos (Crear)
```
Solicitud → Análisis → Estimación → Planificación → Desarrollo → QA → Producción → Cierre
```
> **PMBOK:** Desarrollo de nuevas funcionalidades (Feature delivery)

### Mejoras (Optimizar)
```
Solicitud → Análisis → Estimación → Aprobación → Desarrollo → QA → Producción → Cierre
```
> **PMBOK:** Mejora continua, optimización de procesos existentes

### Backlog (Planificar)
```
Identificación → Priorización → Estimación → Sprint Planning → Desarrollo → Cierre
```
> **PMBOK:** Gestión del alcance - Planificación y priorización

## Calendario de Reuniones

| Reunión | Frecuencia | Día/Hora | Referencia PMBOK |
|---------|------------|----------|------------------|
| Daily Dev | Diaria | Avance + Blockers + Prioridades | Comunicaciones del equipo |
| Cliente Nevasa | Semanal | Martes 16:00 | Gestión de partes interesadas |
| Reporte de estatus | 2x/semana | Lunes y Jueves (mismo formato) | Informes de performance |

### Daily con Equipo Dev
- **Frecuencia:** Diaria
- **Duración:** 15-20 minutos
- **Temas:** Avance, Blockers, Prioridades, Compromisos
- **PMBOK:** Stand-up meeting, sincronización del equipo

### Reunión con Cliente (Martes 16:00)
- **Duración:** 30-45 minutos
- **Agenda:** Incidencias → Evolutivos → Mejoras → Backlog → Próximos pasos
- **PMBOK:** Revisión de partes interesadas, alineación de expectativas

### Envío de Reportes
- **Días:** Lunes y Jueves
- **Mismo formato** para ambos días
- **Contenido:** Resumen ejecutivo, incidencias, evolutivos, mejoras, backlog
- **PMBOK:** Informes de estado del proyecto

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

### Áreas (Orden según prioridad PMBOK)
```
GPI CB
├── Incidencias    ← #1 Corregir (Defectos)
│   ├── Crítica
│   ├── Alta
│   ├── Media
│   └── Baja
├── Evolutivos     ← #2 Crear (Nuevas funcionalidades)
├── Mejoras        ← #3 Optimizar (Mejoras incrementales)
└── Backlog        ← #4 Planificar (Futuro)
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

| Frente | Métrica | Referencia PMBOK |
|--------|---------|------------------|
| Incidencias | Tiempo promedio resolución | Gestión de Calidad |
| Incidencias | % Resueltas en SLA | Acuerdos de Nivel de Servicio |
| Evolutivos | Velocidad (Story Points/Sprint) | Velocidad del equipo |
| Mejoras | Lead time | Tiempo de entrega |
| Backlog | % Completado | Gestión del Alcance |
