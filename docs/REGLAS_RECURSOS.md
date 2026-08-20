# Reglas del Módulo de Recursos

## 1. Estructura de Archivos

| Archivo | Ubicación | Descripción |
|---|---|---|
| `Seguimiento Requerimientos NevasaCB.xlsx` | OneDrive | Archivo fuente (hoja "Recursos") |
| `Reporte_Estatus_GPI_CB.xlsx` | OneDrive | Archivo de salida (hoja "Análisis de Recursos") |
| `generar_recursos.py` | scripts/ | Script generador |

**Ejecución:**
```bash
python scripts/generar_recursos.py
```

---

## 2. Hoja de Recursos en Excel

### Estructura (fila 1 = headers)

| Col | Campo | Tipo | Valores |
|---|---|---|---|
| A | Persona | Texto | Nombre del recurso |
| B | Horas Estimadas | Número | Horas planificadas |
| C | Horas Reales | Número | Horas trabajadas |
| D | Capacidad Semanal | Número | Horas/semana (default: 40) |
| E | Fase Actual | Lista | Cola, Desarrollo, QA, Producción |
| F | Asignado a | Texto | Proyecto o tarea |

---

## 3. Fases del Recurso

| Fase | Color | Descripción |
|---|---|---|
| Cola | Gris `#E8E8E8` | Esperando inicio |
| Desarrollo | Amarillo `#FFFFCC` | En fase de desarrollo |
| QA | Azul `#CCE5FF` | En fase de testing |
| Producción | Verde `#CCFFCC` | En mantenimiento/soporte |

---

## 4. Cálculos

### Utilización
```
Semanas = Horas Reales / HH_DIARIAS / 5
Utilización = (Horas Reales / (Capacidad Semanal × Semanas)) × 100

Donde HH_DIARIAS = 8 (configurado en rutas.py)
```

### Clasificación

| Utilización | Estado | Color |
|---|---|---|
| > 100% | Sobrecargado | Rojo `#FF4444` |
| 80% - 100% | Alta | Naranja `#FF8C00` |
| 50% - 80% | Media | Amarillo `#FFD700` |
| < 50% | Baja | Verde `#90EE90` |

---

## 5. Hoja de Salida: Análisis de Recursos

### Secciones

| # | Sección | Contenido |
|---|---|---|
| 1 | Resumen | Total personas, Horas estimadas/reales, Utilización promedio, Sobrecargados |
| 2 | Distribución por Fase | Cantidad de recursos por fase |
| 3 | Detalle por Persona | Horas, capacidad, utilización, estado |

---

## 6. Métricas

| Métrica | Fórmula |
|---|---|
| Total personas | COUNT(Personas) |
| Horas estimadas | SUM(Horas Estimadas) |
| Horas reales | SUM(Horas Reales) |
| Utilización promedio | AVG(Utilizaciones) |
| Sobrecargados | COUNT(Personas WHERE Utilización > 100%) |

---

## 7. Buenas Prácticas

1. **No sobrecargar**: Mantener utilización < 100%
2. **Balancear carga**: Distribuir horas entre equipo
3. **Anticipar cuellos de botella**: Identificar fases con pocos recursos
4. **Revisar semanalmente**: Actualizar horas reales cada semana

---

## 8. Notas Técnicas

- **Hoja requerida**: Si la hoja "Recursos" no existe, el script muestra aviso
- **Dependencia**: Requiere que el reporte principal ya haya sido generado
- **Default capacidad**: 40 horas/semana si no se especifica
