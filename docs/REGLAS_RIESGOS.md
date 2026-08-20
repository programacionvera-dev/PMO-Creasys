# Reglas del Módulo de Riesgos

## 1. Estructura de Archivos

| Archivo | Ubicación | Descripción |
|---|---|---|
| `Seguimiento Requerimientos NevasaCB.xlsx` | OneDrive | Archivo fuente (hoja "Riesgos") |
| `Reporte_Estatus_GPI_CB.xlsx` | OneDrive | Archivo de salida (hoja "Análisis de Riesgos") |
| `generar_riesgos.py` | scripts/ | Script generador |

**Ejecución:**
```bash
python scripts/generar_riesgos.py
```

---

## 2. Hoja de Riesgos en Excel

### Estructura (fila 1 = headers)

| Col | Campo | Tipo | Valores |
|---|---|---|---|
| A | ID | Texto | RIESGO-001, RIESGO-002, etc. |
| B | Descripción | Texto | Descripción detallada |
| C | Probabilidad | Lista | Baja, Media, Alta |
| D | Impacto | Lista | Bajo, Medio, Alto, Crítico |
| E | Estado | Lista | Abierto, Mitigado, Cerrado |
| F | Mitigación | Texto | Acción implementada |
| G | Responsable | Texto | Persona a cargo |
| H | Fecha Identificación | Fecha | DD/MM/YYYY |
| I | Fecha Cierre | Fecha | DD/MM/YYYY |
| J | Notas | Texto | Observaciones |

---

## 3. Cálculo de Score

```
Score = Probabilidad × Impacto

Probabilidad:
  Baja  = 1
  Media = 2
  Alta  = 3

Impacto:
  Bajo    = 1
  Medio   = 2
  Alto    = 3
  Crítico = 4

Rango del Score: 1 - 12
```

---

## 4. Clasificación de Riesgos

| Score | Clasificación | Color Fondo | Color Texto |
|---|---|---|---|
| 7 - 12 | Crítico | Rojo `#FF4444` | Blanco |
| 4 - 6 | Alto | Naranja `#FF8C00` | Blanco |
| 2 - 3 | Medio | Amarillo `#FFD700` | Negro |
| 1 | Bajo | Verde `#90EE90` | Negro |

---

## 5. Estados del Riesgo

| Estado | Color | Descripción |
|---|---|---|
| Abierto | Rosa `#FFCCCC` | Requiere atención activa |
| Mitigado | Amarillo `#FFFFCC` | Acción implementada |
| Cerrado | Verde `#CCFFCC` | Ya no aplica |

---

## 6. Hoja de Salida: Análisis de Riesgos

### Secciones

| # | Sección | Contenido |
|---|---|---|
| 1 | Resumen | Total, Abiertos, Mitigados, Cerrados, Críticos, Score Promedio |
| 2 | Detalle | Lista de riesgos ordenados por score (descendente) |

---

## 7. Métricas

| Métrica | Fórmula |
|---|---|
| Total riesgos | COUNT(Riesgos) |
| Riesgos abiertos | COUNT(Riesgos WHERE Estado = "Abierto") |
| Riesgos críticos | COUNT(Riesgos WHERE Score >= 7) |
| % mitigados | (Mitigados / Total) × 100 |
| Score promedio | AVERAGE(Scores) |

---

## 8. Notas Técnicas

- **Hoja requerida**: Si la hoja "Riesgos" no existe, el script muestra aviso y termina
- **Dependencia**: Requiere que el reporte principal ya haya sido generado
- **Encoding**: Maneja caracteres especiales (tildes, ñ)
