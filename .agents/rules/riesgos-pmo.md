# Reglas de Riesgos PMO

## Estructura de Datos

### Hoja: Riesgos

| Columna | Tipo | Descripción |
|---|---|---|
| ID | Texto | Identificador único del riesgo |
| Descripción | Texto | Descripción detallada del riesgo |
| Probabilidad | Lista | Baja / Media / Alta |
| Impacto | Lista | Bajo / Medio / Alto / Crítico |
| Estado | Lista | Abierto / Mitigado / Cerrado |
| Mitigación | Texto | Acción de mitigación implementada o planificada |
| Responsable | Texto | Persona a cargo del seguimiento |
| Fecha Identificación | Fecha | Cuándo se identificó el riesgo |
| Fecha Cierre | Fecha | Cuándo se cerró (si aplica) |
| Notas | Texto | Observaciones adicionales |

## Cálculo de Score

```
Score = Probabilidad × Impacto

Valores:
  Probabilidad: Baja=1, Media=2, Alta=3
  Impacto: Bajo=1, Medio=2, Alto=3, Crítico=4

Rango: 1 - 12
```

## Clasificación de Riesgos

| Score | Clasificación | Color |
|---|---|---|
| 7 - 12 | Crítico | Rojo |
| 4 - 6 | Alto | Naranja |
| 2 - 3 | Medio | Amarillo |
| 1 | Bajo | Verde |

## Estados del Riesgo

| Estado | Descripción |
|---|---|
| Abierto | Riesgo identificado, requiere atención |
| Mitigado | Acción de mitigación implementada |
| Cerrado | Riesgo ya no aplica o fue resuelto |

## Métricas

- **Total riesgos**: Cantidad total registrados
- **Riesgos abiertos**: Requieren atención activa
- **Riesgos críticos**: Score ≥ 7
- **% mitigados**: (Mitigados / Total) × 100
- **Score promedio**: Promedio de todos los scores
