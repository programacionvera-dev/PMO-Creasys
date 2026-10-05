# Flujo de Trabajo PMO - GPI CB

## 1. Contexto

Sistema informático para el mercado financiero (Nevasa). El proyecto se encuentra en Producción con múltiples frentes de trabajo activos.

### Frentes de Trabajo

Basado en **PMBOK 7ª Edición** - Gestión de Entregas y **Azure DevOps Best Practices**:

| # | Frente | Tipo Azure DevOps | Prioridad PMBOK | Descripción |
|---|--------|-------------------|-----------------|-------------|
| 1 | **Incidencias** | Bug | #1 - Corregir | Defectos, bugs, problemas en producción |
| 2 | **Evolutivos** | Feature | #2 - Crear | Nuevas funcionalidades, valor nuevo al negocio |
| 3 | **Mejoras** | Product Backlog Item | #3 - Optimizar | Mejoras incrementales a funcionalidad existente |
| 4 | **Backlog** | Task | #4 - Planificar | Ideas, tareas pendientes de priorizar |

> **Referencia PMBOK:** Gestión de la Calidad - Los defectos (incidencias) tienen prioridad sobre nuevas funcionalidades para mantener la estabilidad del sistema en producción.

### Regla Fundamental
> **Las incidencias siempre tienen prioridad sobre cualquier otro requerimiento.**
> *Alineado con PMBOK: Gestión de Riesgos - Mitigar problemas críticos antes de agregar nueva funcionalidad.*

---

## 2. Definición por Frente

### 2.1 INCIDENCIAS (Prioridad #1 - Corregir)
**Qué es:** Error o mal funcionamiento reportado por el cliente.
**PMBOK:** Gestión de Calidad - Control de defectos

**Ejemplos:**
- Error al generar un reporte
- Sistema no responde
- Datos incorrectos en pantalla
- Botón no funciona

**Responsable:** Equipo de desarrollo + QA

---

### 2.2 EVOLUTIVOS (Prioridad #2 - Crear)
**Qué es:** Nueva funcionalidad o módulo solicitado por el cliente.
**PMBOK:** Gestión de Entregas - Crear valor nuevo

**Ejemplos:**
- Nuevo módulo de consultas
- Integración con sistema externo
- Nuevos tipos de reportes
- Automatización de proceso

**Responsable:** Equipo de desarrollo + Análisis + Arquitectura

---

### 2.3 MEJORAS (Prioridad #3 - Optimizar)
**Qué es:** Solicitud de ajuste o optimización a funcionalidad existente.
**PMBOK:** Mejora Continua - Optimizar procesos

**Ejemplos:**
- Cambiar formato de un reporte
- Agregar filtro adicional
- Modificar validación existente
- Ajustar layout de pantalla

**Responsable:** Equipo de desarrollo + Análisis

---

### 2.4 BACKLOG (Prioridad #4 - Planificar)
**Qué es:** Pendientes internos que no son solicitados por el cliente.
**PMBOK:** Gestión del Alcance - Planificación

**Ejemplos:**
- Refactoring de código
- Optimización de base de datos
- Actualización de dependencias
- Mejoras técnicas

**Responsable:** Equipo de desarrollo

---

## 3. Flujo por Frente

### 3.1 INCIDENCIAS (Prioridad #1 - Corregir)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  RECEPCIÓN  │───→│ DIAGNÓSTICO │───→│ DESARROLLO  │───→│     QA      │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                                                                 ▼
                    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
                    │   CIERRE    │←───│ PRODUCCIÓN  │←───│CERTIFICACIÓN│
                    └─────────────┘    └─────────────┘    └─────────────┘
```

**Pasos detallados:**

| Paso | Acción | Responsable | Herramienta |
|------|--------|-------------|-------------|
| 1 | Cliente reporta incidencia | Cliente | Email/Soporte |
| 2 | Registrar en Azure DevOps como Bug | PMO/Soporte | Azure DevOps |
| 3 | Asignar severidad | PMO | Azure DevOps |
| 4 | Diagnóstico técnico | Tech Lead | Azure DevOps |
| 5 | Desarrollar solución | Desarrollador | VS Code / Azure DevOps |
| 6 | Pruebas enCertificación | QA | Azure DevOps |
| 7 | Desplegar a Producción | DevOps | Pipelines |
| 8 | Notificar cierre al cliente | PMO | Email |

---

### 3.2 EVOLUTIVOS (Prioridad #2 - Crear)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ SOLICITUD   │───→│   ANÁLISIS  │───→│ ESTIMACIÓN  │───→│PLANIFICACIÓN│
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                                                                 ▼
                    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
                    │   CIERRE    │←───│ PRODUCCIÓN  │←───│ DESARROLLO  │
                    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                                                                 ▼
                                                           ┌─────────────┐
                                                           │     QA      │
                                                           └─────────────┘
```

**Pasos detallados:**

| Paso | Acción | Responsable | Herramienta |
|------|--------|-------------|-------------|
| 1 | Cliente solicita evolutivo | Cliente | Email/Reunión |
| 2 | Registrar en Azure DevOps como Feature | PMO | Azure DevOps |
| 3 | Análisis detallado | Analista + Arquitecto | Azure DevOps |
| 4 | Estimar esfuerzo (Story Points) | Tech Lead | Azure DevOps |
| 5 | Planificar en roadmap | PMO | Excel/Power BI |
| 6 | Aprobar con cliente | PMO | Reunión |
| 7 | Desarrollar (puede ser múltiples sprints) | Desarrollador | VS Code |
| 8 | Pruebas enCertificación | QA | Azure DevOps |
| 9 | Desplegar a Producción | DevOps | Pipelines |
| 10 | Notificar al cliente | PMO | Email |

---

### 3.3 MEJORAS (Prioridad #3 - Optimizar)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ SOLICITUD   │───→│   ANÁLISIS  │───→│ ESTIMACIÓN  │───→│APROBACIÓN   │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                                                                 ▼
                    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
                    │   CIERRE    │←───│ PRODUCCIÓN  │←───│ DESARROLLO  │
                    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                                                                 ▼
                                                           ┌─────────────┐
                                                           │     QA      │
                                                           └─────────────┘
```

**Pasos detallados:**

| Paso | Acción | Responsable | Herramienta |
|------|--------|-------------|-------------|
| 1 | Cliente solicita mejora | Cliente | Email/Reunión |
| 2 | Registrar en Azure DevOps como PBI | PMO | Azure DevOps |
| 3 | Analizar requisito | Analista | Azure DevOps |
| 4 | Estimar esfuerzo (Story Points) | Tech Lead | Azure DevOps |
| 5 | Aprobar con cliente | PMO | Reunión |
| 6 | Desarrollar en sprint actual | Desarrollador | VS Code |
| 7 | Pruebas enCertificación | QA | Azure DevOps |
| 8 | Desplegar a Producción | DevOps | Pipelines |
| 9 | Notificar al cliente | PMO | Email |

---

### 3.4 BACKLOG (Prioridad #4 - Planificar)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│IDENTIFICACIÓN│───→│PRIORIZACIÓN │───→│ ESTIMACIÓN  │───→│   SPRINT    │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                                                                 ▼
                    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
                    │   CIERRE    │←───│ DESARROLLO  │←───│  PLANNING   │
                    └─────────────┘    └─────────────┘    └─────────────┘
```

**Pasos detallados:**

| Paso | Acción | Responsable | Herramienta |
|------|--------|-------------|-------------|
| 1 | Identificar pendiente interno | Tech Lead/Desarrollador | Azure DevOps |
| 2 | Registrar como Task o PBI | PMO | Azure DevOps |
| 3 | Priorizar con cliente (opcional) | PMO | Reunión semanal |
| 4 | Estimar esfuerzo | Tech Lead | Azure DevOps |
| 5 | Asignar a sprint | PMO | Azure DevOps |
| 6 | Desarrollar | Desarrollador | VS Code |
| 7 | Cerrar tarea | PMO | Azure DevOps |

---

## 4. Calendario de Reuniones

### 4.1 Calendario Semanal

| Día | Actividad | Hora | Participantes |
|---|---|---|---|
| Lunes | Envío reporte de estatus | -- | PMO → Cliente |
| Martes | Daily + Reunión cliente | 16:00 | PMO, Tech Lead, Cliente |
| Miércoles | Daily | -- | Equipo Dev |
| Jueves | Envío reporte de estatus | -- | PMO → Cliente |
| Viernes | Daily + Cierre de semana | -- | Equipo Dev |

### 4.2 Daily con Equipo Dev

**Frecuencia:** Diaria
**Duración:** 15-20 minutos
**Participantes:** PMO, Tech Lead, Desarrolladores

**Temas (formato completo):**
1. **Avance:** Qué se hizo ayer
2. **Blockers:** Qué está deteniendo el progreso
3. **Prioridades:** Qué se hace hoy
4. **Compromisos:** Entregas del día

### 4.3 Reunión con Cliente (Martes 16:00)

**Frecuencia:** Semanal
**Duración:** 30-45 minutos
**Participantes:** PMO, Tech Lead, Cliente (Nevasa)

**Agenda (orden según prioridad PMBOK):**

| # | Tema | Duración | Responsable |
|---|------|----------|-------------|
| 1 | Review incidencias de la semana (#1 Corregir) | 10 min | PMO |
| 2 | Estado de evolutivos en curso (#2 Crear) | 10 min | PMO |
| 3 | Estado de mejoras en curso (#3 Optimizar) | 10 min | PMO + Tech Lead |
| 4 | Revisar backlog pendiente (#4 Planificar) | 5 min | PMO |
| 5 | Próximos pasos y compromisos | 5 min | PMO + Tech Lead |

**Salida esperada:**
- [ ] Backlog priorizado en Azure DevOps
- [ ] Incidencias asignadas
- [ ] Compromisos confirmados con cliente

### 4.4 Envío de Reportes de Estatus

**Frecuencia:** Lunes y Jueves
**Mismo formato para ambos días**

**Contenido del reporte (orden según prioridad PMBOK):**
1. Resumen ejecutivo (métricas)
2. Incidencias abiertas/cerradas (#1 Corregir)
3. Evolutivos en progreso (#2 Crear)
4. Mejoras en progreso (#3 Optimizar)
5. Estado del backlog (#4 Planificar)

### 4.5 Checklist Semanal

#### Lunes
- [ ] Revisar incidencias nuevas
- [ ] Actualizar estado en Azure DevOps
- [ ] **Enviar reporte de estatus**

#### Martes
- [ ] Daily con equipo
- [ ] Ejecutar reunión con cliente (16:00)
- [ ] Actualizar prioridades en Azure DevOps

#### Miércoles
- [ ] Daily con equipo
- [ ] Seguimiento a tareas asignadas
- [ ] Validar entregas en Certificación

#### Jueves
- [ ] Daily con equipo
- [ ] **Enviar reporte de estatus**
- [ ] Documentar lecciones aprendidas

#### Viernes
- [ ] Daily con equipo
- [ ] Cierre de semana
- [ ] Preparar agenda para próxima semana

---

## 5. Integración con Azure DevOps

### 5.1 Estructura de Áreas (Orden según prioridad PMBOK)

```
GPI CB (Proyecto)
├── Incidencias    ← #1 Corregir (Defectos)
│   ├── Crítica
│   ├── Alta
│   ├── Media
│   └── Baja
├── Evolutivos     ← #2 Crear (Nuevas funcionalidades)
├── Mejoras        ← #3 Optimizar (Mejoras incrementales)
└── Backlog        ← #4 Planificar (Futuro)
```

### 5.2 Tipos de Trabajo

| Azure DevOps | Frente | Prioridad PMBOK | Uso |
|--------------|--------|-----------------|-----|
| Bug | Incidencias | #1 - Corregir | Errores reportados |
| Feature | Evolutivos | #2 - Crear | Nuevas funcionalidades |
| Product Backlog Item | Mejoras | #3 - Optimizar | Mejoras a existente |
| Task | Backlog | #4 - Planificar | Tareas internas |

### 5.3 Campos Personalizados

| Campo | Tipo | Valores |
|-------|------|---------|
| Severidad | Picklist | Crítica, Alta, Media, Baja |
| Cliente | String | Nevasa |
| Sprint | Iteration | Sprint 1, Sprint 2, etc. |
| Estado Producción | Boolean | Sí/No |

### 5.4 Queries Útiles

```sql
-- Incidencias abiertas (#1 Corregir)
SELECT * FROM WorkItems
WHERE [System.TeamProject] = 'GPI CB'
AND [System.WorkItemType] = 'Bug'
AND [System.State] <> 'Closed'

-- Evolutivos en progreso (#2 Crear)
SELECT * FROM WorkItems
WHERE [System.TeamProject] = 'GPI CB'
AND [System.WorkItemType] = 'Feature'
AND [System.State] = 'Active'

-- Mejoras pendientes (#3 Optimizar)
SELECT * FROM WorkItems
WHERE [System.TeamProject] = 'GPI CB'
AND [System.WorkItemType] = 'Product Backlog Item'
AND [System.State] = 'New'
```

---

## 6. Comunicación con Cliente

### 6.1 Email Semanal (Template)

**Asunto:** `GPI CB - Resumen Semanal [Fecha]`

**Contenido (orden según prioridad PMBOK):**

```html
<h2>Resumen Semanal GPI CB</h2>
<p><strong>Período:</strong> [Fecha Inicio] - [Fecha Fin]</p>

<h3>1. Incidencias (#1 - Corregir)</h3>
<ul>
    <li>Resueltas esta semana: [N]</li>
    <li>Abiertas: [N]</li>
    <li>Críticas pendientes: [N]</li>
</ul>

<h3>2. Evolutivos (#2 - Crear)</h3>
<ul>
    <li>En planificación: [N]</li>
    <li>En desarrollo: [N]</li>
</ul>

<h3>3. Mejoras (#3 - Optimizar)</h3>
<ul>
    <li>En desarrollo: [N]</li>
    <li>Completadas: [N]</li>
</ul>

<h3>4. Próximos Pasos (#4 - Planificar)</h3>
<ul>
    <li>[Tarea 1]</li>
    <li>[Tarea 2]</li>
</ul>
```

### 6.2 Frecuencia de Comunicación

| Tipo | Frecuencia | Canal |
|------|------------|-------|
| Resumen semanal | Semanal | Email |
| Incidencia crítica | Inmediata | Email + Llamada |
| Reunión de avance | Semanal | Teams/Zoom |
| Reporte mensual | Mensual | Power BI |

---

## 7. Métricas de Seguimiento

### 7.1 Métricas por Frente

| Frente | Prioridad PMBOK | Métrica | Fórmula |
|--------|-----------------|---------|---------|
| Incidencias | #1 - Corregir | Tiempo promedio resolución | AVG(Fecha Cierre - Fecha Apertura) |
| Incidencias | #1 - Corregir | % Resueltas en SLA | (Resueltas en SLA / Total) × 100 |
| Evolutivos | #2 - Crear | Velocidad | Story Points completados / Sprint |
| Mejoras | #3 - Optimizar | Lead time | AVG(Fecha Producción - Fecha Solicitud) |
| Backlog | #4 - Planificar | % Completado | (Completados / Total) × 100 |

### 7.2 Dashboard Power BI

**Tablas necesarias:**
- Datos (ya existe)
- Riesgos (ya existe)
- Lessons Learned (ya existe)
- Recursos (ya existe)
- **Incidencias** (nueva - opcional)

---

## 8. Checklist Semanal

### Lunes
- [ ] Revisar incidencias nuevas
- [ ] Actualizar estado en Azure DevOps
- [ ] Preparar agenda de reunión

### Martes (Reunión)
- [ ] Ejecutar reunión semanal
- [ ] Actualizar prioridades en Azure DevOps
- [ ] Enviar comunicado al cliente

### Miércoles - Viernes
- [ ] Seguimiento a tareas asignadas
- [ ] Validar entregas enCertificación
- [ ] Documentar lecciones aprendidas

---

## 9. Notas Importantes

1. **Incidencias siempre primero**: No importa qué tan urgente sea un evolutivo o mejora, una incidencia tiene prioridad.
   *Referencia PMBOK: Gestión de Riesgos - Mitigar problemas críticos antes de crear nuevo valor.*

2. **Documentar todo**: Cada interacción con el cliente, cada decisión, cada cambio debe quedar registrado en Azure DevOps.

3. **Comunicar progreso**: El cliente debe saber qué estamos haciendo y cuándo estará listo.

4. **Aprender de errores**: Cada incidencia debe generar una lección aprendida si es relevante.

5. **Revisar SLAs**: Verificar semanalmente que se cumplen los tiempos acordados.
