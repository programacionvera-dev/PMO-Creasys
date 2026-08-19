# Reglas PMO Nevasa

## Mapeo de Columnas (0-based index)
- `valores[0]`: Índice
- `valores[1]`: Requerimiento
- `valores[2]`: Detalle
- `valores[3]`: Área
- `valores[4]`: Solicitante
- `valores[5]`: Categoría
- `valores[6]`: Prioridad
- `valores[8]`: Asignado
- `valores[9]`: Etapa
- `valores[11]`: Fecha Recepción
- `valores[14]`: Estimado Fin Desarrollo
- `valores[17]`: Real Inicio
- `valores[18]`: Fecha Real QA
- `valores[19]`: Aprobado PaP
- `valores[20]`: Fecha Producción
- `valores[25]`: Historia
- `valores[27]`: Periodo

## Reglas de Negocio

### Estados
- **Completado**: Producción, Certificación Nevasa
- **En Progreso**: Sin Formalizar, Análisis, Desarrollo, Certificación Creasys, Stand By, Cancelado
- **Pendiente**: Pendiente

### Disclaimer
"Los requerimientos en 'Certificación Nevasa' se consideran completados ya que para Creasys representan entrega final del desarrollo."

### Filtros
- **QA**: `etapa == 'Certificación Nevasa'`
- **Producción**: `etapa == 'Producción' and not item['fecha_produccion']`

### Prioridad
- 0 → MÁXIMA
- 1 → ALTA
- empty/None/`Sin Prioridad` → `Sin Prioridad`
