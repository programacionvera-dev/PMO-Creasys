# Guia Power BI - Seguimiento Nevasa

## 1. Configuracion Inicial

### Importar Datos
1. Abrir Power BI Desktop
2. **Obtener datos** > **Excel**
3. Seleccionar: `Datos_PowerBI_Nevasa.xlsx`
4. Cargar tabla **Datos**
5. Cargar tablas **Dim_Area**, **Dim_Etapa**, **Dim_Prioridad**

### Crear Relaciones
- `Datos[Area]` > `Dim_Area[Area]`
- `Datos[Etapa]` > `Dim_Etapa[Etapa]`
- `Datos[Prioridad]` > `Dim_Prioridad[Prioridad]`

---

## 2. Medidas DAX

### KPIs Principales

```dax
Total Requerimientos = COUNTROWS(Datos)
```

```dax
Completados = 
CALCULATE(COUNTROWS(Datos), Datos[Etapa] = "Produccion")
```

```dax
En Progreso = 
CALCULATE(
    COUNTROWS(Datos),
    Datos[Etapa] IN {"Desarrollo", "Certificacion Creasys", "Certificacion Nevasa", "Analisis"}
)
```

```dax
Pendientes = 
CALCULATE(COUNTROWS(Datos), Datos[Etapa] = "Pendiente")
```

```dax
% Completados = DIVIDE([Completados], [Total Requerimientos])
```

### Metricas de Tiempo

```dax
Tiempo Promedio Ciclo = 
AVERAGEX(
    FILTER(Datos, NOT(ISBLANK(Datos[Ciclo_Total]))),
    Datos[Ciclo_Total]
)
```

```dax
Tiempo Promedio Desarrollo = 
AVERAGEX(
    FILTER(Datos, NOT(ISBLANK(Datos[Desarrollo_Real]))),
    Datos[Desarrollo_Real]
)
```

```dax
Tiempo Promedio Cola = 
AVERAGEX(
    FILTER(Datos, NOT(ISBLANK(Datos[Cola_Real]))),
    Datos[Cola_Real]
)
```

```dax
Tiempo Promedio QA = 
AVERAGEX(
    FILTER(Datos, NOT(ISBLANK(Datos[QA_Real]))),
    Datos[QA_Real]
)
```

### Precision de Estimaciones

```dax
% A Tiempo = 
DIVIDE(
    CALCULATE(COUNTROWS(Datos), Datos[A_Tiempo] = "Si"),
    CALCULATE(COUNTROWS(Datos), NOT(ISBLANK(Datos[A_Tiempo])))
)
```

```dax
Varianza Promedio Dias = 
AVERAGEX(
    FILTER(Datos, NOT(ISBLANK(Datos[Varianza_Dias]))),
    Datos[Varianza_Dias]
)
```

```dax
Horas Totales Reales = SUM(Datos[Horas_Reales])
```

```dax
Horas Totales Estimadas = SUM(Datos[Horas_Estimadas])
```

```dax
Desviacion Horas = [Horas Totales Reales] - [Horas Totales Estimadas]
```

### Metricas por Fase

```dax
Dias Cola Promedio = 
AVERAGEX(
    FILTER(Datos, NOT(ISBLANK(Datos[Cola_Real]))),
    Datos[Cola_Real]
)
```

```dax
Dias Desarrollo Promedio = 
AVERAGEX(
    FILTER(Datos, NOT(ISBLANK(Datos[Desarrollo_Real]))),
    Datos[Desarrollo_Real]
)
```

```dax
Dias QA Promedio = 
AVERAGEX(
    FILTER(Datos, NOT(ISBLANK(Datos[QA_Real]))),
    Datos[QA_Real]
)
```

---

## 3. Reportes Sugeridos

### Reporte 1: Dashboard Principal

| Visual | Ubicacion | Metrica |
|--------|-----------|---------|
| KPI Card | Arriba izquierda | Total Requerimientos |
| KPI Card | Arriba centro | % Completados |
| KPI Card | Arriba derecha | Tiempo Promedio Ciclo |
| Bar Chart | Medio izquierda | Req. por Etapa |
| Bar Chart | Medio derecha | Req. por Area |
| Table | Abajo | Top 10 Requerimientos |

### Reporte 2: Analisis de Tiempos

| Visual | Ubicacion | Metrica |
|--------|-----------|---------|
| Gauge | Arriba izquierda | % A Tiempo |
| Gauge | Arriba centro | Varianza Promedio Dias |
| Gauge | Arriba derecha | Desviacion Horas |
| Stacked Bar | Medio | Dias por Fase (Cola, Desarrollo, QA) |
| Scatter | Abajo | Duracion Estimada vs Real |
| Table | Abajo | Detalle por Requerimiento |

### Reporte 3: Tendencia y Carga

| Visual | Ubicacion | Metrica |
|--------|-----------|---------|
| Line Chart | Arriba | Req. Recibidos vs Completados por Periodo |
| Bar Chart | Medio izquierda | Horas por Desarrollador |
| Bar Chart | Medio derecha | Horas por Area |
| Pie Chart | Abajo | Distribucion por Prioridad |

### Reporte 4: Analisis por Dimension

| Visual | Ubicacion | Metrica |
|--------|-----------|---------|
| Treemap | Arriba | Distribucion por Area x Etapa |
| Bar Chart | Medio | Tiempo Promedio por Aplicativo |
| Bar Chart | Medio | Tiempo Promedio por Categoria |
| Table | Abajo | Detalle por Area |

---

## 4. Formato Recomendado

### Colores por Etapa
- Produccion: Verde `#00B050`
- Certificacion Nevasa: Azul `#4472C4`
- Certificacion Creasys: Azul claro `#5B9BD5`
- Desarrollo: Naranja `#ED7D31`
- Analisis: Amarillo `#FFC000`
- Pendiente: Gris `#A5A5A5`
- Stand By: Gris oscuro `#7F7F7F`
- Cancelado: Rojo `#FF0000`

### Colores por Prioridad
- Maxima: Rojo `#FF0000`
- Alta: Naranja `#ED7D31`
- Media/Alta: Amarillo `#FFC000`
- Media: Azul `#4472C4`
- Baja: Verde `#00B050`
- Sin Prioridad: Gris `#A5A5A5`

---

## 5. Actualizacion de Datos

Para actualizar los reportes:
1. Ejecutar: `python scripts/generar_datos_powerbi.py`
2. Abrir Power BI Desktop
3. **Transformar datos** > **Cerrar y aplicar**
4. Los datos se actualizan automaticamente

---

## 6. Archivos Incluidos

| Archivo | Descripcion |
|---------|-------------|
| `scripts/generar_datos_powerbi.py` | Generador de datos para Power BI |
| `Datos_PowerBI_Nevasa.xlsx` | Datos pre-calculados |
| `Guia_PowerBI_Nevasa.md` | Esta guia |
