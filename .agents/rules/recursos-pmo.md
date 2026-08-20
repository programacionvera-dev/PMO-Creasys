# Reglas de Recursos PMO

## Estructura de Datos

### Hoja: Recursos

| Columna | Tipo | Descripción |
|---|---|---|
| Persona | Texto | Nombre del recurso |
| Horas Estimadas | Número | Horas planificadas para el trabajo |
| Horas Reales | Número | Horas efectivamente trabajadas |
| Capacidad Semanal | Número | Horas disponibles por semana (default: 40) |
| Fase Actual | Lista | Cola / Desarrollo / QA / Producción |
| Asignado a | Texto | Proyecto o tarea asignada |

## Fases del Recurso

| Fase | Descripción | Color |
|---|---|---|
| Cola | Esperando inicio | Gris |
| Desarrollo | En fase de desarrollo | Amarillo |
| QA | En fase de testing | Azul |
| Producción | En mantenimiento/soporte | Verde |

## Cálculos

### Utilización
```
Semanas = Horas Reales / HH_DIARIAS / 5
Utilización = (Horas Reales / (Capacidad Semanal × Semanas)) × 100
```

### Clasificación por Utilización

| Utilización | Estado | Color |
|---|---|---|
| > 100% | Sobrecargado | Rojo |
| 80% - 100% | Alta | Naranja |
| 50% - 80% | Media | Amarillo |
| < 50% | Baja | Verde |

## Métricas

- **Total personas**: Cantidad de recursos asignados
- **Horas estimadas vs reales**: Comparación planificación vs ejecución
- **Utilización promedio**: Promedio de utilización del equipo
- **Sobrecargados**: Personas con utilización > 100%
- **Distribución por fase**: Cuántos recursos en cada fase

## Buenas Prácticas

1. **No sobrecargar**: Mantener utilización < 100%
2. **Balancear carga**: Distribuir horas entre equipo
3. **Anticipar cuellos de botella**: Identificar fases con pocos recursos
4. **Revisar semanalmente**: Actualizar horas reales cada semana
