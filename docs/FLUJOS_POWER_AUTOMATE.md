# Flujos Power Automate - GPI CB

## Resumen General

Este documento describe todos los flujos de Power Automate configurados y planificados para el proyecto GPI CB.

---

## Arquitectura General

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ARQUITECTURA POWER AUTOMATE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     FLUJOS DE NOTIFICACIÓN                          │   │
│  │                                                                     │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │ CERTIFICACIÓN │  │ PRODUCCIÓN   │  │   ESTATUS    │              │   │
│  │  │    (QA)      │  │              │  │   CLIENTE    │              │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │   │
│  │         │                 │                 │                       │   │
│  │         └─────────────────┼─────────────────┘                       │   │
│  │                           │                                         │   │
│  └───────────────────────────┼─────────────────────────────────────────┘   │
│                              │                                             │
│                              ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     FLUJOS DE ENTRADA                               │   │
│  │                                                                     │   │
│  │  ┌──────────────┐                                                   │   │
│  │  │  RECEPCIÓN   │ ← Pendiente aprobación                           │   │
│  │  │ (Automático) │                                                   │   │
│  │  └──────────────┘                                                   │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     FLUJOS FUTUROS                                  │   │
│  │                                                                     │   │
│  │  ┌──────────────┐                                                   │   │
│  │  │ AZURE DEVOPS │ ← Requiere licencia                              │   │
│  │  │   (API)      │                                                   │   │
│  │  └──────────────┘                                                   │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Flujos Activos

### 1. Notificación de Certificación QA

| Aspecto | Detalle |
|---------|---------|
| **Nombre** | `NEVASA - Notificación Certificación` |
| **Estado** | ✅ Activo |
| **Trigger** | Programado (Martes 9:00 AM Chile) |
| **Frecuencia** | Semanal |

#### Proceso

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    PYTHON    │    │   ONEDRIVE   │    │ POWERAUTOMATE│    │   OUTLOOK    │
│  Genera HTML │───→│  Sincroniza  │───→│  Lee HTML    │───→│  Envía correo│
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

#### Acciones

| # | Paso | Descripción |
|---|------|-------------|
| 1 | Ejecutar script | `python generar_plantillascorreo.py` genera `qa.html` |
| 2 | Sincronizar | OneDrive sincroniza HTML automáticamente |
| 3 | Trigger | Power Automate se dispara (Martes 9AM) |
| 4 | Leer HTML | Lee `plantillas_correo/qa.html` |
| 5 | Leer Excel | Filtra filas con Etapa = "Certificación Nevasa" o "Certificación Creasys" y Aprobado PAP vacío |
| 6 | Buscar PDFs | Por cada fila con plan, busca en `/Planes De Prueba/` |
| 7 | Crear links | Genera enlaces anónimos para cada PDF |
| 8 | Reemplazar | Sustituye `{{PLAN:...}}` por URLs reales |
| 9 | Enviar | Envía 1 correo HTML con firma |

#### Configuración

- **Para:** *(Configurar destinatarios)*
- **Asunto:** `NVSCB [Certificación]: Requerimientos Disponibles Certificación Nevasa`
- **¿Es HTML?:** Sí

---

### 2. Notificación de Producción

| Aspecto | Detalle |
|---------|---------|
| **Nombre** | `NEVASA - Notificación Producción` |
| **Estado** | ✅ Activo |
| **Trigger** | Programado (configurar frecuencia) |
| **Frecuencia** | Semanal/según necesidad |

#### Proceso

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    PYTHON    │    │   ONEDRIVE   │    │ POWERAUTOMATE│    │   OUTLOOK    │
│  Genera HTML │───→│  Sincroniza  │───→│  Lee HTML    │───→│  Envía correo│
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

#### Acciones

| # | Paso | Descripción |
|---|------|-------------|
| 1 | Ejecutar script | `python generar_plantillascorreo.py` genera `produccion.html` |
| 2 | Sincronizar | OneDrive sincroniza HTML automáticamente |
| 3 | Trigger | Power Automate se dispara |
| 4 | Leer HTML | Lee `plantillas_correo/produccion.html` |
| 5 | Enviar | Envía 1 correo HTML con firma |

#### Configuración

- **Para:** *(Configurar destinatarios)*
- **Asunto:** `NVSCB [Producción]: Requerimientos a Producción`
- **¿Es HTML?:** Sí

---

### 3. Notificación de Estatus al Cliente

| Aspecto | Detalle |
|---------|---------|
| **Nombre** | `NEVASA - Reporte de Estatus` |
| **Estado** | ✅ Activo |
| **Trigger** | Programado (Lunes y Jueves) |
| **Frecuencia** | 2 veces por semana |

#### Proceso

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    PYTHON    │    │   ONEDRIVE   │    │ POWERAUTOMATE│    │   OUTLOOK    │
│ Genera HTML  │───→│  Sincroniza  │───→│ Lee HTML +   │───→│ Envía correo │
│ + Excel      │    │  ambos       │    │ Excel        │    │ + adjunto    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

#### Acciones

| # | Paso | Descripción |
|---|------|-------------|
| 1 | Ejecutar script reporte | `python generar_reporte_nevasa.py` genera `Reporte_Estatus_GPI_CB.xlsx` |
| 2 | Ejecutar script HTML | `python generar_plantillascorreo.py` genera `reporte_estatus.html` |
| 3 | Sincronizar | OneDrive sincroniza ambos archivos |
| 4 | Trigger | Power Automate se dispara |
| 5 | Leer HTML | Lee `plantillas_correo/reporte_estatus.html` |
| 6 | Leer Excel | Lee `Reporte_Estatus_GPI_CB.xlsx` |
| 7 | Enviar | Envía correo HTML con reporte adjunto |

#### Configuración

- **Para:** *(Configurar destinatarios)*
- **Asunto:** `GPI CB - Reporte de Estatus [Fecha]`
- **¿Es HTML?:** Sí
- **Adjunto:** `Reporte_Estatus_GPI_CB.xlsx`

---

## Flujo Pendiente de Aprobación

### 4. Recepción Automática de Requerimientos

| Aspecto | Detalle |
|---------|---------|
| **Nombre** | `NEVASA - Recepción Automática` |
| **Estado** | ⏸ Pendiente aprobación |
| **Trigger** | Correo entrante en buzón compartido |
| **Frecuencia** | Cada vez que llega un correo |

#### Proceso

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   CLIENTE    │───→│ POWERAUTOMATE│───→│   EXCEL      │───→│   PLANNER    │
│  (email)     │    │  (buzón)     │    │  (registro)  │    │  (tarjeta)   │
└──────────────┘    └──────┬───────┘    └──────────────┘    └──────────────┘
                           │
                           ├──────────────→ Auto-respuesta al cliente
                           │
                           └──────────────→ Notificación Teams
```

#### Acciones

| # | Acción | Herramienta | Descripción |
|---|--------|-------------|-------------|
| 1 | Trigger | Outlook | Correo entrante en buzón compartido |
| 2 | Auto-responder | Outlook | Responde automáticamente al cliente |
| 3 | Registrar | Excel Online | Agrega registro en Seguimiento Requerimientos NevasaCB |
| 4 | Crear tarjeta | Planner | Crea tarea con información del requerimiento |
| 5 | Notificar | Teams | Envía mensaje al grupo/equipo |

#### Mapeo de Datos

| Campo Correo | Campo Excel | Fórmula/Expresión |
|--------------|-------------|-------------------|
| Asunto | Requerimiento | `triggerOutputs()?['subject']` |
| Cuerpo (texto plano) | Detalle | `triggerOutputs()?['bodyPreview']` |
| Remitente | Solicitante | `triggerOutputs()?['from']` |
| Fecha | Fecha Recepción | `utcNow()` |
| (auto) | Estado | `"Pendiente"` |
| (auto) | Etapa | `"Sin Formalizar"` |

#### Configuración Requerida

| Componente | Acción |
|------------|--------|
| Buzón compartido | Crear en Outlook y configurar permisos |
| Excel | Verificar tabla `SeguimientoNevasaCB` |
| Planner | Crear plan/tablero para tarjetas |
| Teams | Identificar canal de notificaciones |

---

## Flujo Futuro (Mejora)

### 5. Integración Azure DevOps

| Aspecto | Detalle |
|---------|---------|
| **Nombre** | `NEVASA - Azure DevOps Sync` |
| **Estado** | 🔮 Futuro (requiere licencia) |
| **Trigger** | Manual o al registrar en Excel |
| **Frecuencia** | Según necesidad |

#### Descripción

Integración de Power Automate con la API de Azure DevOps para crear Work Items automáticamente.

#### Beneficios

- Sincronización automática Excel ↔ Azure DevOps
- Creación de tarjetas con toda la información
- Tracking en tiempo real
- Métricas automáticas

#### Requisitos

| Requisito | Descripción |
|-----------|-------------|
| Licencia Azure DevOps | Plan de pago requerido |
| Personal Access Token (PAT) | Token de autenticación |
| Configuración API | Endpoint y permisos |

#### Endpoint de la API

```
POST https://dev.azure.com/{org}/{project}/_apis/wit/workitems/$Bug?api-version=7.0
```

---

## Dependencias entre Flujos

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPENDENCIAS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PYTHON (scripts)                                               │
│  ├─ generar_plantillascorreo.py                                 │
│  │   ├─ Genera: qa.html → Flujo 1 (Certificación)              │
│  │   ├─ Genera: produccion.html → Flujo 2 (Producción)         │
│  │   └─ Genera: reporte_estatus.html → Flujo 3 (Estatus)       │
│  │                                                              │
│  └─ generar_reporte_nevasa.py                                   │
│      └─ Genera: Reporte_Estatus_GPI_CB.xlsx → Flujo 3 (Estatus)│
│                                                                 │
│  POWER AUTOMATE                                                 │
│  ├─ Flujo 1 (Certificación) → Usa HTML de Python               │
│  ├─ Flujo 2 (Producción) → Usa HTML de Python                  │
│  ├─ Flujo 3 (Estatus) → Usa HTML + Excel de Python             │
│  └─ Flujo 4 (Recepción) → Independiente (genera Excel)         │
│                                                                 │
│  ONEDRIVE                                                       │
│  ├─ plantillas_correo/ → HTMLs generados por Python             │
│  ├─ Reporte_Estatus_GPI_CB.xlsx → Reporte generado por Python  │
│  └─ Seguimiento Requerimientos NevasaCB.xlsx → Excel fuente    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Checklist de Implementación

### Flujos Activos

- [ ] Flujo 1: Configurar destinatarios
- [ ] Flujo 1: Verificar schedule (Martes 9AM)
- [ ] Flujo 2: Configurar destinatarios
- [ ] Flujo 2: Definir frecuencia
- [ ] Flujo 3: Configurar destinatarios
- [ ] Flujo 3: Verificar schedule (Lunes/Jueves)

### Flujo Pendiente

- [ ] Flujo 4: Crear buzón compartido
- [ ] Flujo 4: Configurar permisos
- [ ] Flujo 4: Crear plan en Planner
- [ ] Flujo 4: Identificar canal en Teams
- [ ] Flujo 4: Aprobar ejecución

### Flujo Futuro

- [ ] Flujo 5: Obtener licencia Azure DevOps
- [ ] Flujo 5: Crear Personal Access Token
- [ ] Flujo 5: Configurar endpoint API
- [ ] Flujo 5: Implementar integración

---

## Solución de Problemas Comunes

### Flujo no se dispara

1. Verificar que el schedule esté activo
2. Verificar zona horaria
3. Revisar historial de ejecuciones

### HTML no se actualiza

1. Verificar que Python se ejecutó correctamente
2. Verificar sincronización de OneDrive
3. Revisar nombre del archivo

### Correo no llega

1. Verificar permisos de Outlook
2. Verificar dirección del destinatario
3. Revisar carpeta de spam

### Excel no se actualiza

1. Verificar que la tabla existe en el Excel
2. Verificar nombres de las columnas
3. Revisar permisos de edición
