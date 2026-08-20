# Reglas de Lessons Learned PMO

## Estructura de Datos

### Hoja: Lessons Learned

| Columna | Tipo | Descripción |
|---|---|---|
| ID | Texto | Identificador único |
| Fecha | Fecha | Fecha del registro |
| Categoría | Lista | Técnico / Proceso / Comunicación / Recurso / Cliente |
| Descripción | Texto | Qué pasó (contexto del evento) |
| Impacto | Texto | Cuál fue el impacto en el proyecto |
| Lección | Texto | Qué aprendimos de la experiencia |
| Acción Correctiva | Texto | Qué haremos diferente la próxima vez |
| Aplicable a | Texto | Cliente/Proyecto específico o "General" |
| Registrado por | Texto | Quién registró la lección |

## Categorías

| Categoría | Descripción | Ejemplo |
|---|---|---|
| Técnico | Issues de tecnología, herramientas, integraciones | "La API falla con payloads > 1MB" |
| Proceso | Problemas en flujos de trabajo, metodología | "Falta de revisión antes de producción" |
| Comunicación | Problemas de comunicación con stakeholders | "Requerimiento no fue entendido correctamente" |
| Recurso | Issues de disponibilidad, capacidad, habilidades | "Faltó conocimiento en tecnología X" |
| Cliente | Lecciones específicas del cliente | "El cliente prefiere reuniones semanales" |

## Métricas

- **Total lecciones**: Cantidad total registradas
- **Con acción correctiva**: Lecciones que tienen plan de acción
- **% con acción**: (Con acción / Total) × 100
- **Por categoría**: Distribución por tipo de lección

## Uso

1. Registrar lecciones durante o después de cada sprint/fase
2. Revisar lecciones anteriores al iniciar nuevo proyecto/cliente
3. Aplicar acciones correctivas en procesos actuales
4. Compartir lecciones "General" con todo el equipo
