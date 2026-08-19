# Reglas del Reporte Ejecutivo GPI CB

## 1. Estructura de Archivos

| Archivo | Ubicación | Descripción |
|---|---|---|
| `Seguimiento Nevasa 2026.xlsx` | Misma carpeta | Archivo fuente (lectura) |
| `Reporte_Estatus_GPI_CB.xlsx` | Misma carpeta | Archivo de salida (se sobrescribe) |
| `generar_reporte_nevasa.py` | Misma carpeta | Script generador |

**Ejecución:**
```bash
python generar_reporte_nevasa.py
```

---

## 2. Hojas del Reporte

| Hoja | Contenido |
|---|---|
| Resumen Ejecutivo | Métricas, indicadores, distribuciones |
| Detalle por Área | Listado de requerimientos por área |

---

## 3. Clasificación de Estados

| Estado Fuente | Clasificación |
|---|---|
| Producción | Completado |
| Terminado | Completado |
| QA Nevasa | En Progreso |
| En Desarrollo | En Progreso |
| En Revisión | En Progreso |
| Integración | En Progreso |
| Pendiente | Pendiente |
| Eliminado | Pendiente |

---

## 4. Mapeo de Columnas (Fuente → Reporte)

| Columna Fuente | Nombre Original | Columna Reporte |
|---|---|---|
| A | Periodo | Periodo |
| B | Tipo | Tipo |
| C | Prioridad | Prioridad |
| D | Area | Área |
| E | Fecha solicitud/revisión | Fecha Solicitud |
| F | Quien Solicita | Solicitante |
| G | Requerimiento/Asunto | Requerimiento |
| H | Detalle Requerimiento | Detalle Requerimiento |
| I | Responsable | (no se usa) |
| J | Fecha Inicio Ejecución | Fecha Inicio Ejecución |
| K | Fecha Entrega QA | Fecha Entrega QA |
| L | Estado | Estado |
| M | Historia | Observaciones |
| N | Fecha Entrega Producción | Fecha Entrega Producción |

---

## 5. Valores de Prioridad

| Valor Fuente | Prioridad Asignada |
|---|---|
| 0 | MÁXIMA |
| 1 | ALTA |
| (vacío) | SP |
| Otro valor | Se conserva tal cual |

---

## 6. Indicador del Proyecto (5 Etapas)

| % Completados | Indicador | Color Fondo | Color Texto |
|---|---|---|---|
| < 20% | CRÍTICO | Rojo `#FF4444` | Blanco |
| 20% - 39% | ALERTA | Naranja `#FF8C00` | Blanco |
| 40% - 59% | REQUIERE ATENCIÓN | Amarillo `#FFD700` | Negro |
| 60% - 79% | EN DESARROLLO | Verde claro `#90EE90` | Negro |
| >= 80% | SATISFACTORIO | Verde `#228B22` | Blanco |

**Cálculo:** `% Cumplimiento = (Completados / Total) * 100`

---

## 7. Distribución por Tipo (Matriz)

### Columnas
| Columna | Descripción |
|---|---|
| Tipo | Incidencia, Solicitud, Requerimiento |
| Total | Cantidad total por tipo |
| % Producción | % que llegó a Producción |
| Pendiente | Cantidad en estado Pendiente |
| QA Nevasa | Cantidad en estado QA Nevasa |
| En Desarrollo | Cantidad en estado En Desarrollo |
| Producción | Cantidad en estado Producción/Terminado |

### Reglas de Color (% Producción)
| % Producción | Color Texto |
|---|---|
| < 40% | Rojo `#FF0000` |
| 40% - 79% | Ámbar `#CC8000` |
| >= 80% | Verde `#008000` |

### Énfasis
- **Incidencia** y **Solicitud**: Texto en **negrita**
- **Requerimiento**: Texto normal

---

## 8. Ordenamiento en Detalle por Área

### Grupo 1 (Primeras filas) - Con orden de prioridad
| Estado | Orden | Prioridades |
|---|---|---|
| Pendiente | 0 | MÁXIMA → ALTA → MEDIA/ALTA → MEDIA → BAJA → SP |
| En Desarrollo | 1 | MÁXIMA → ALTA → MEDIA/ALTA → MEDIA → BAJA → SP |
| QA Creasys | 2 | MÁXIMA → ALTA → MEDIA/ALTA → MEDIA → BAJA → SP |

### Grupo 2 (Últimas filas) - Sin orden de prioridad
| Estado | Orden |
|---|---|
| QA Nevasa | 0 |
| Producción | 1 |
| Terminado | 2 |

### Orden de Columnas
| # | Columna | Alineación |
|---|---|---|
| 1 | # | Centro |
| 2 | Prioridad | Centro |
| 3 | Requerimiento | Izquierda, centrado vertical |
| 4 | Detalle Requerimiento | Izquierda, centrado vertical, wrap text |
| 5 | Solicitante | Centro |
| 6 | Estado | Centro |
| 7 | Fecha Solicitud | Centro |
| 8 | Fecha Inicio Ejecución | Centro |
| 9 | Fecha Entrega QA | Centro |
| 10 | Fecha Entrega Producción | Centro |
| 11 | Periodo | Centro |
| 12 | Observaciones | Izquierda, centrado vertical, wrap text |

---

## 9. Formato General

### Colores Base
| Elemento | Color |
|---|---|
| Azul oscuro (headers) | `#2F5496` |
| Azul claro (totales) | `#D6E4F0` |
| Texto header | Blanco `#FFFFFF` |

### Colores Condicionales (Estados)
| Estado | Color Fondo |
|---|---|
| Pendiente | Rosa `#FFCCCC` |
| En Desarrollo | Amarillo `#FFFFCC` |
| En Revisión | Crema `#FFF8DC` |
| QA Nevasa | Azul claro `#CCE5FF` |
| Producción | Verde claro `#CCFFCC` |
| Terminado | Verde `#90EE90` |

### Colores Condicionales (Prioridad)
| Prioridad | Color Fondo |
|---|---|
| MÁXIMA | Rosa `#FFB6C1` |
| ALTA | Naranja claro `#FFDAB9` |

### Fuentes
| Elemento | Fuente | Tamaño | Negrita |
|---|---|---|---|
| Título principal | Calibri | 16 | Sí |
| Secciones | Calibri | 11 | Sí |
| Headers tabla | Calibri | 9 | Sí |
| Datos | Calibri | 9 | No |

---

## 10. Tabla de Escalas (Resumen Ejecutivo)

Ubicación: Columnas M-N, desde fila 8

| Rango | Indicador | Color |
|---|---|---|
| < 20% | CRÍTICO | Rojo |
| 20% - 39% | ALERTA | Naranja |
| 40% - 59% | REQUIERE ATENCIÓN | Amarillo |
| 60% - 79% | EN DESARROLLO | Verde claro |
| >= 80% | SATISFACTORIO | Verde |

---

## 11. Secciones del Resumen Ejecutivo

| # | Sección | Columnas |
|---|---|---|
| 1 | Métricas Generales | Total, Completados, En Progreso, Pendientes, % Cumplimiento |
| 2 | Estado General del Proyecto | Indicador con color |
| 3 | Distribución por Estado | Estado, Cantidad, % del Total |
| 4 | Distribución por Área | Área, Total, Pendiente, En Progreso, Completado |
| 5 | Distribución por Período | Período, Total, Pendiente, En Progreso, Completado |
| 6 | Distribución por Prioridad | Prioridad, Cantidad, % del Total |
| 7 | Distribución por Tipo | Matriz Tipo × Estado con % Producción |

---

## 12. Notas Técnicas

- **Encoding:** El archivo fuente puede tener variaciones de encoding (ej: "Producción" vs "Producci�n"). El script maneja estas variaciones.
- **Archivo bloqueado:** Si el Excel fuente está abierto, el script fallará con error de permisos.
- **Fecha de generación:** Se actualiza automáticamente al ejecutar el script.
