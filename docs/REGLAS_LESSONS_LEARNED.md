# Reglas del Módulo de Lessons Learned

## 1. Estructura de Archivos

| Archivo | Ubicación | Descripción |
|---|---|---|
| `Seguimiento Requerimientos NevasaCB.xlsx` | OneDrive | Archivo fuente (hoja "Lessons Learned") |
| `Reporte_Estatus_GPI_CB.xlsx` | OneDrive | Archivo de salida (hoja "Lessons Learned") |
| `generar_lessons_learned.py` | scripts/ | Script generador |

**Ejecución:**
```bash
python scripts/generar_lessons_learned.py
```

---

## 2. Hoja de Lessons Learned en Excel

### Estructura (fila 1 = headers)

| Col | Campo | Tipo | Valores |
|---|---|---|---|
| A | ID | Texto | LL-001, LL-002, etc. |
| B | Fecha | Fecha | DD/MM/YYYY |
| C | Categoría | Lista | Técnico, Proceso, Comunicación, Recurso, Cliente |
| D | Descripción | Texto | Qué pasó |
| E | Impacto | Texto | Cuál fue el impacto |
| F | Lección | Texto | Qué aprendimos |
| G | Acción Correctiva | Texto | Qué haremos diferente |
| H | Aplicable a | Texto | Cliente/Proyecto o "General" |
| I | Registrado por | Texto | Quién registró |

---

## 3. Categorías

| Categoría | Color | Descripción |
|---|---|---|
| Técnico | Azul claro `#CCE5FF` | Tecnología, herramientas, integraciones |
| Proceso | Amarillo `#FFFFCC` | Flujos de trabajo, metodología |
| Comunicación | Gris claro `#E8E8E8` | Comunicación con stakeholders |
| Recurso | Crema `#FFF8DC` | Disponibilidad, capacidad, habilidades |
| Cliente | Verde claro `#CCFFCC` | Específico del cliente |

---

## 4. Hoja de Salida: Lessons Learned

### Secciones

| # | Sección | Contenido |
|---|---|---|
| 1 | Resumen | Total lecciones, Con acción correctiva, % Con acción |
| 2 | Distribución por Categoría | Cantidad y % por categoría |
| 3 | Detalle | Lista completa de lecciones |

---

## 5. Métricas

| Métrica | Fórmula |
|---|---|
| Total lecciones | COUNT(Lessons) |
| Con acción correctiva | COUNT(Lessons WHERE Acción Correctiva != "") |
| % con acción | (Con acción / Total) × 100 |
| Por categoría | GROUP BY Categoría |

---

## 6. Buenas Prácticas

1. **Registrar**: Después de cada sprint, fase o evento significativo
2. **Revisar**: Al iniciar nuevo proyecto o cliente
3. **Aplicar**: Implementar acciones correctivas en procesos
4. **Compartir**: Lecciones "General" son para todo el equipo

---

## 7. Notas Técnicas

- **Hoja requerida**: Si la hoja "Lessons Learned" no existe, el script muestra aviso
- **Dependencia**: Requiere que el reporte principal ya haya sido generado
- **Filtros**: Se pueden filtrar por categoría, cliente, período
