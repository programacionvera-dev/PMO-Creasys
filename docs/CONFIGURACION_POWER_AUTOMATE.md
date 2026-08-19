# Configuración Power Automate - Enlaces de Descarga de Planes de Prueba

## Resumen

Este documento describe cómo configurar Power Automate para generar enlaces de descarga anónimos para los planes de prueba almacenados en OneDrive.

**Versión Simplificada:** No usa acciones "Compose" (no disponibles en tu entorno).

**Trigger:** Programado (Cada Martes 9:00 AM Chile).

---

## Flujo Completo de Ejecución

### Diagrama del Proceso

```
┌─────────────────────────────────────────────────────────────────┐
│           FLUJO NEVASA - CERTIFICACIÓN QA                       │
│           Trigger: Martes 9:00 AM Chile                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   EXCEL      │    │   PYTHON     │    │  ONE DRIVE    │      │
│  │ Seguimiento  │───→│  Genera HTML │───→│  qa.html      │      │
│  │ NevasaCB     │    │  con placeholders                     │      │
│  └──────────────┘    └──────────────┘    └──────┬───────┘      │
│                                                  │              │
│                                                  ▼              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  SCHEDULE    │    │ POWER AUTOMATE│    │  ONE DRIVE    │      │
│  │  Martes 9AM  │───→│  Trigger:    │───→│  Lee HTML     │      │
│  │  Chile       │    │  Recurrence  │    │               │      │
│  └──────────────┘    └──────────────┘    └──────┬───────┘      │
│                                                  │              │
│                                                  ▼              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  EXCEL       │    │ POWER AUTOMATE│    │  ONE DRIVE    │      │
│  │  Lee filas   │───→│  Loop 1:     │───→│  Busca PDFs  │      │
│  │  Certif.     │    │  Por cada    │    │  en /Planes/  │      │
│  └──────────────┘    │  fila        │    └──────────────┘      │
│                      └──────┬───────┘                           │
│                             │                                   │
│                             ▼                                   │
│                      ┌──────────────┐    ┌──────────────┐      │
│                      │ POWER AUTOMATE│    │  ONE DRIVE    │      │
│                      │  Loop 2:     │───→│  Crea links  │      │
│                      │  Reemplaza   │    │  anónimos    │      │
│                      │  placeholders│    └──────────────┘      │
│                      └──────┬───────┘                           │
│                             │                                   │
│                             ▼                                   │
│                      ┌──────────────┐    ┌──────────────┐      │
│                      │ POWER AUTOMATE│    │  OUTLOOK      │      │
│                      │  Envía correo│───→│  Correo HTML  │      │
│                      │  (1 vez)     │    │  + firma CID  │      │
│                      └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Secuencia de Ejecución

| # | Paso | Componente | Descripción |
|---|------|------------|-------------|
| 1 | Ejecutar Python | Local | `python generar_plantillascorreo.py` genera `qa.html` con placeholders |
| 2 | Subir a OneDrive | OneDrive | Los HTML se sincronizan automáticamente a OneDrive |
| 3 | **Disparador** | **Power Automate** | **Recurrence: Cada Martes 9:00 AM Chile** |
| 4 | Leer HTML | Power Automate | Lee `plantillas_correo/qa.html` desde OneDrive |
| 5 | Leer Excel | Power Automate | Lee filas con Etapa = "Certificación Nevasa" |
| 6 | Buscar PDFs | OneDrive | Por cada fila con plan, busca en `/Planes De Prueba/{AÑO}/{MES}/` |
| 7 | Crear links | OneDrive | Genera enlace anónimo View-only para cada PDF encontrado |
| 8 | Reemplazar | Power Automate | Sustituye `{{PLAN:...}}` por URLs reales en el HTML |
| 9 | Enviar | Outlook | Envía **1 correo** HTML con firma embebida |

### Dependencias Críticas

| Componente | Requisito | Riesgo si falla |
|------------|-----------|-----------------|
| Python | Ejecutarse ANTES del schedule | HTML sin datos actualizados |
| OneDrive | Sincronización automática | HTML desactualizado |
| Excel | Campo "Plan de Prueba" = nombre exacto del PDF | Links no generados |
| SharePoint | "Anyone with the link" habilitado | No se pueden crear links |
| Outlook | Permisos de envío | No se envían correos |

---

## Nombres de Acciones en Español

| Nombre en Inglés | Nombre en Español (Power Automate) |
|------------------|-----------------------------------|
| List rows present in a table | Enumerar las filas de una tabla |
| List files in folder | **Mostrar los archivos de la carpeta** |
| Create sharing link for a file | **Crear un vínculo para compartir** |
| Condition | Condición |
| Apply to each | Aplicar a cada uno |
| Initialize variable | Inicializar variable |
| Append to array variable | Agregar a variable de arreglo |
| Get file content | Obtener contenido del archivo |
| Send an email (V2) | Enviar un correo electrónico (V2) |

---

## Flujo Completo

```
1. Trigger: Recurrence (Programado)
   - Frecuencia: Semanal
   - Día: Martes
   - Hora: 09:00 AM
   - Zona horaria: Chile (Pacific Standard Time)
2. Obtener contenido del HTML (OneDrive)
3. Leer Excel de Seguimiento
4. Variable: Mapeo de meses en español (MesesEspanol)
5. Variable: Array para almacenar resultados (ArrayPlanes)
6. Variable: FechaPeriodo (vacía)

--- PRIMER LOOP: Por cada fila del Excel ---
7. Aplicar a cada uno (loop por cada fila del Excel)
   a. Condición: Verificar si Plan de Prueba Y Periodo tienen valor
   b. [SI] Establecer variable FechaPeriodo
   c. [SI] Obtener metadatos de carpeta (para obtener identificador)
   d. [SI] Mostrar archivos de la carpeta (usando identificador)
   e. Condición: Archivo encontrado?
   f. [SI] For each (por cada archivo en body/value)
      │   i.  Crear vínculo para compartir (con Id del archivo)
      │   ii. Anexar a variable ArrayPlanes (NameNoExt + URL web)
   g. [NO] No hacer nada (saltar fila)

--- SEGUNDO LOOP: Por cada placeholder ---
8. Aplicar a cada uno (loop por cada placeholder en ArrayPlanes)
   a. Obtener contenido actual del HTML
   b. Actualizar archivo con replace()

--- ENVÍO DE CORREO (fuera de loops) ---
9. Enviar correo con HTML modificado (1 vez)
   - La firma se incluye automáticamente en el HTML (URL web directa)
```

---

## Configuración Paso a Paso

### Paso 1: Trigger (Programado)

- **Acción:** Recurrence (Programado)
- **Frecuencia:** Week (Semanal)
- **Intervalo:** 1
- **Día:** Tuesday (Martes)
- **Hora:** 09:00
- **Timezone:** Pacific Standard Time (Chile)
- **StartTime:** Configurar después de pruebas manuales

**Configuración en Power Automate:**
1. Crear nuevo flow → **Scheduled cloud flow**
2. Nombre: `NEVASA - Notificación QA`
3. Run this flow: *(dejar para después de pruebas)*
4. Repeat every: `1 Week`
5. On these days: `Tuesday`
6. At: `09:00 AM`
7. Show advanced options → Time zone: `Pacific Standard Time`

### Paso 2: Obtener contenido del HTML

- **Acción:** Obtener contenido del archivo (OneDrive)
- **Ubicación:** Tu OneDrive for Business
- **Archivo:** `plantillas_correo/qa.html` o `produccion.html`

### Paso 3: Leer Excel de Seguimiento

- **Acción:** Enumerar las filas de una tabla (Excel Online - Empresa)
- **Ubicación:** OneDrive for Business
- **Biblioteca de documentos:** OneDrive
- **Archivo:** `/Gestión Nevasa/Gestión y Revisión/Seguimiento Requerimientos NevasaCB.xlsx`
- **Tabla:** SeguimientoNevasaCB
- **Consulta de filtro:** `Etapa eq 'Certificación Nevasa'`

### Paso 4: Variable - Mapeo de Meses

- **Acción:** Inicializar variable
- **Nombre:** `MesesEspanol`
- **Tipo:** `Object`
- **Valor:**
```json
{
  "01": "ENERO",
  "02": "FEBRERO",
  "03": "MARZO",
  "04": "ABRIL",
  "05": "MAYO",
  "06": "JUNIO",
  "07": "JULIO",
  "08": "AGOSTO",
  "09": "SEPTIEMBRE",
  "10": "OCTUBRE",
  "11": "NOVIEMBRE",
  "12": "DICIEMBRE"
}
```

> **Nota:** Los meses del 01 al 09 tienen cero a la izquierda para coincidir con el formato `MM` de `formatDateTime`.

### Paso 5: Variable - Array de Planes

- **Acción:** Inicializar variable
- **Nombre:** `ArrayPlanes`
- **Tipo:** `Array`
- **Valor:** `[]` (arreglo vacío)

### Paso 6: Variable - FechaPeriodo

- **Acción:** Inicializar variable
- **Nombre:** `FechaPeriodo`
- **Tipo:** `String`
- **Valor:** _(dejar vacío)_

---

### Paso 7: Aplicar a cada uno (Loop) - SIMPLIFICADO

Este es el paso más complejo. Se ejecuta por cada fila del Excel.

---

#### 6.1 Crear el Loop

**Acción:** Aplicar a cada uno

**Seleccionar output:** Copiar y pegar:
```
@{body('Leer_excel_seguimiento')?['value']}
```

---

#### Dentro del Loop - Acciones en orden:

---

##### 6.2 Condición: Verificar si Plan de Prueba y Periodo tienen valor

**Acción:** Condición

**Condición (usar expresión fx):**
```
@and(not(empty(items('Aplicar_a_cada_uno')?['Plan de Prueba'])), not(empty(items('Aplicar_a_cada_uno')?['Periodo'])))
```

**Cómo configurar:**
1. Haz clic en el campo izquierdo
2. Haz clic en el ícono **fx** (funciones)
3. Pega la expresión de arriba

**Explicación:** Verifica que AMBOS campos tengan valor (Plan de Prueba Y Periodo).

---

##### 6.3 [SI] Establecer variable FechaPeriodo

**Acción:** Establecer variable

| Campo | Valor |
|-------|-------|
| **Nombre** | `FechaPeriodo` |
| **Valor** | Ver expresión abajo |

**Expresión:**
```
@{formatDateTime(addDays('1899-12-30', int(items('Aplicar_a_cada_uno')?['Periodo']), 'yyyy-MM-dd'), 'yyyy-MM-dd')}
```

**Explicación:**
- `int(items('Aplicar_a_cada_uno')?['Periodo'])` convierte el número serial de Excel a entero
- `addDays('1899-12-30', ...)` convierte el número serial a fecha real
- `formatDateTime(..., 'yyyy-MM-dd')` **fuerza** el formato ISO (ej: `2026-07-01`)

> **IMPORTANTE:** El `formatDateTime` al final es OBLIGATORIO para que la fecha esté en formato `yyyy-MM-dd` y no en formato legible como "July 1".

---

##### 6.4 [SI] Obtener metadatos de archivo mediante ruta de acceso

**Acción:** Obtener metadatos de archivo mediante ruta de acceso - OneDrive para la Empresa

| Campo | Valor |
|-------|-------|
| **Ruta del archivo** | Ver expresión abajo |

**Expresión para Ruta del archivo (copiar y pegar):**
```
@{concat('/Gestión Nevasa/Planes De Prueba/', formatDateTime(variables('FechaPeriodo'), 'yyyy'), '/', variables('MesesEspanol')[string(int(formatDateTime(variables('FechaPeriodo'), 'MM')))])}
```

**Ejemplo de resultado:** `/Gestión Nevasa/Planes De Prueba/2026/JULIO`

> **Nota:** Esta acción obtiene el identificador de la carpeta necesario para el siguiente paso.
> Es requerida porque la ruta contiene caracteres especiales (tilde en "Gestión").

---

##### 6.5 [SI] Mostrar los archivos de la carpeta

**Acción:** Mostrar los archivos de la carpeta - OneDrive para la Empresa

| Campo | Valor |
|-------|-------|
| **Carpeta** | Seleccionar **Identificador** del paso "Obtener metadatos" |

**Configuración:**
1. Haz clic en el campo **Carpeta**
2. Selecciona **Contenido dinámico**
3. Busca y selecciona **Identificador** de la acción "Obtener metadatos de archivo mediante ruta de acceso"

> **IMPORTANTE:** NO escribas la ruta directamente. Usa el contenido dinámico "Identificador" del paso anterior.

---

##### 6.6 [SI] Condición: Archivo encontrado

**Acción:** Condición

**Expresión para el campo izquierdo (copiar y pegar):**
```
@not(empty(body('Mostrar_los_archivos_de_la_carpeta')?['value']))
```

| Campo | Valor |
|-------|-------|
| **Campo izquierdo** | Expresión: `@not(empty(body('Mostrar_los_archivos_de_la_carpeta')?['value']))` |
| **Operador** | `es igual a` |
| **Campo derecho** | `true` |

**Explicación:**
- `body('...')?['value']` obtiene el array de archivos encontrados
- `empty(...)` verifica si el array está vacío
- `not(...)` invierte el resultado: `true` si hay archivos, `false` si está vacío
- La condición compara con `true` para continuar solo si hay archivos

---

##### 6.7 [SI][SI] For each - Por cada archivo encontrado

**Acción:** Aplicar a cada uno (For each)

**Seleccionar una salida de los pasos anteriores:** Seleccionar **`value`** de Dynamic Content de "Mostrar los archivos de la carpeta"

> **Importante:** Este loop itera sobre CADA archivo encontrado en la carpeta, creando un vínculo individual para cada uno.

---

###### 6.7.1 [SI][SI] Crear un vínculo para compartir

**Acción:** Crear un vínculo para compartir - OneDrive para la Empresa

| Campo | Valor |
|-------|-------|
| **Archivo** | Seleccionar **`Id`** de Dynamic Content (del item actual del For each) |
| **Tipo de vínculo** | `View` |
| **Ámbito de vínculo** | `Anonymous` |

**Configuración:**
1. Haz clic en el campo **Archivo**
2. Selecciona **Contenido dinámico**
3. Busca **`Id`** de "Aplicar a cada uno" (el item actual del loop)

**Explicación:**
- `Id` obtiene el identificador de cada archivo en la iteración
- `View` = Solo lectura (no editable)
- `Anonymous` = Acceso anónimo (cualquiera con el vínculo puede descargar)

> **⚠️ Seguridad - Enlaces con Expiración:**
> Power Automate no soporta configuración de expiración directamente en esta acción.
> Para mejorar la seguridad, configurar la política de enlaces a nivel de SharePoint Admin Center:
> 1. Ir a Microsoft 365 Admin Center → SharePoint Admin Center
> 2. Policies → Sharing
> 3. En "Links" → Seleccionar "Anyone with the link can view" y configurar expiración (ej: 30 días)
> 4. Esto aplicará a todos los enlaces anónimos creados por Power Automate

---

###### 6.7.2 [SI][SI] Anexar a variable ArrayPlanes

**Acción:** Anexar a la variable de matriz (Append to array variable)

**Nombre de la variable:** `ArrayPlanes`

**Valor:** SeleccionarDynamic Content:

**Estructura del JSON:**
```json
{
  "placeholder": "{{PLAN:NameNoExt}}",
  "url": "URL web"
}
```

**Configuración:**
1. En el campo `placeholder`, escribe `{{PLAN:` + selecciona **`NameNoExt`** de Dynamic Content (del item actual del For each) + `}}`
2. En el campo `url`, selecciona **`URL web`** de Dynamic Content (de "Crear un vínculo para compartir")

| Campo | Dynamic Content | Origen |
|-------|-----------------|--------|
| `placeholder` | `{{PLAN:` + **`NameNoExt`** + `}}` | Item actual del For each |
| `url` | **`URL web`** | "Crear un vínculo para compartir" |

**Ejemplo de resultado:**
```json
{
  "placeholder": "{{PLAN:PP_GPIWEBCB_NVS-T12015 Revision Dividendos}}",
  "url": "https://creasys-my.sharepoint.com/:b:/g/personal/fvera_creasys_cl/..."
}
```

---

## Estructura Visual Completa

```
1. Obtener contenido del HTML (original)
2. Leer Excel de Seguimiento
3. Inicializar variable MesesEspanol = {1:ENERO, ...}
4. Inicializar variable ArrayPlanes = []
5. Inicializar variable FechaPeriodo = ""

═══════════════════════════════════════════════════════
PRIMER LOOP: Por cada fila del Excel
═══════════════════════════════════════════════════════
6. Aplicar a cada uno (filas del Excel)
   │
   ├─ Condición: Plan de Prueba Y Periodo tienen valor?
   │   │
   │   ├─ [SI]
   │   │   │
   │   │   ├─ Establecer variable FechaPeriodo
   │   │   │
   │   │   ├─ Mostrar los archivos de la carpeta
   │   │   │   - Carpeta: /Planes De Prueba/2026/JULIO
   │   │   │
   │   │   ├─ Condición: Archivo encontrado?
   │   │   │   │
   │   │   │   ├─ [SI]
   │   │   │   │   ├─ Crear un vínculo para compartir
   │   │   │   │   └─ Agregar a ArrayPlanes
   │   │   │   │
   │   │   │   └─ [NO] (no hacer nada)
   │   │   │
   │   │   └─ (fin)
   │   │
   │   └─ [NO] (no hacer nada)
   │
   └─ (fin del primer loop)

═══════════════════════════════════════════════════════
SEGUNDO LOOP: Por cada placeholder en ArrayPlanes
═══════════════════════════════════════════════════════
7. Aplicar a cada uno (ArrayPlanes)
   │
   ├─ 7.1 Obtener contenido del HTML actualizado
   └─ 7.2 Actualizar archivo con replace()

═══════════════════════════════════════════════════════
8. Enviar correo
═══════════════════════════════════════════════════════
```

---

### Paso 7: Reemplazar placeholders (Segundo Loop)

Ahora que tenemos el array con todos los placeholder y URLs, reemplazamos en el HTML. Este es un **SEGUNDO loop** separado al del paso 6.

**Acción:** Aplicar a cada uno

**Seleccionar output:**
```
@{variables('ArrayPlanes')}
```

**Dentro de ESTE nuevo loop:**

#### 7.1 Obtener contenido actual del HTML

**Acción:** Obtener contenido del archivo (OneDrive)

| Campo | Valor |
|-------|-------|
| **Archivo** | `plantillas_correo/qa.html` |

> **Nota:** Esta acción debe estar DENTRO del segundo loop para obtener el contenido actualizado con los reemplazos anteriores.

#### 7.2 Actualizar archivo con reemplazo

**Acción:** Actualizar archivo (OneDrive)

| Campo | Valor |
|-------|-------|
| **Archivo** | `plantillas_correo/qa.html` |
| **Contenido del archivo** | Ver expresión abajo |

**Expresión para Contenido del archivo (copiar y pegar):**
```
@{replace(body('Obtener_contenido_del_archivo'), item()?['placeholder'], item()?['url'])}
```

**Explicación:**
- `body('Obtener_contenido_del_archivo')` obtiene el contenido actual del HTML
- `item()?['placeholder']` es el placeholder a reemplazar (ej: `{{PLAN:...}}`)
- `item()?['url']` es la URL del enlace de compartición

> **Importante:** El nombre de la acción "Obtener_contenido_del_archivo" debe coincidir con el nombre exacto de la acción que creaste en el paso 7.1.

---

### Paso 8: Enviar correo (V2)

**Acción:** Enviar un correo electrónico (V2) - Outlook

| Campo | Valor |
|-------|-------|
| **Para** | *(Configurar destinatarios después de pruebas)* |
| **Asunto** | `NVSCB [Certificación]: Requerimientos Listos para Certificación Nevasa` |
| **Cuerpo** | Ver abajo |
| **¿Es HTML?** | `Sí` ← **IMPORTANTE** |

> **Nota:** La firma se incluye automáticamente en el HTML (URL web directa). No se requiere adjuntar imagen.

---

#### Configuración del Cuerpo (Body):

1. Haz clic en **"Mostrar opciones avanzadas"** (Show advanced options)
2. Busca la opción **"Is HTML"** o **"¿Es HTML?"** y seleccióna **`Yes`** o **`Sí`**
3. En el campo **Body** (Cuerpo), escribe la expresión:

**Expresión:**
```
@{body('Obtener_contenido_del_archivo')}
```

> **Nota:** Selecciona la salida de la acción "Obtener_contenido_del_archivo" (paso 8.1 dentro del segundo loop).

---

## Configuración Requerida en OneDrive

### Allow Anyone Links

1. Ir a Microsoft 365 Admin Center
2. SharePoint Admin Center
3. Policies → Sharing
4. Habilitar: "Anyone with the link can access content without signing in"

### Permisos del Flow

- La cuenta que ejecuta el flow tiene acceso a:
  - OneDrive for Business (lectura de archivos)
  - Excel de Seguimiento (lectura)
  - Correo compartido (envío)

---

## Placeholders Generados por Python

### Ejemplo 1: Con plan de prueba
```html
<a href="{{PLAN:PP_GPIWEBCB_NVS-T12015 Revision Dividendos}}">Descargar Plan de Prueba</a>
```

### Ejemplo 2: Con plan de prueba
```html
<a href="{{PLAN:PP_GPIWEBCB_NVS-T12427 Migrar Reporte Comisiones}}">Descargar Plan de Prueba</a>
```

### Ejemplo 3: Sin plan de prueba
```html
-
```

---

## Resultado Final Después de Power Automate

```html
<!-- Antes -->
<a href="{{PLAN:PP_GPIWEBCB_NVS-T12015 Revision Dividendos}}">Descargar Plan de Prueba</a>

<!-- Después -->
<a href="https://creasys-my.sharepoint.com/:b:/g/personal/fvera_creasys_cl/...">Descargar Plan de Prueba</a>
```

---

## Resumen de Acciones por Paso

| Paso | Acción (Español) | Tipo | Loop |
|------|------------------|------|------|
| 1 | **Recurrence** (Programado: Martes 9AM Chile) | Trigger | - |
| 2 | Obtener contenido del archivo (HTML) | OneDrive | - |
| 3 | Enumerar las filas de una tabla | Excel Online | - |
| 4 | Inicializar variable (`MesesEspanol`) | Variable | - |
| 5 | Inicializar variable (`ArrayPlanes`) | Variable | - |
| 6 | Inicializar variable (`FechaPeriodo`) | Variable | - |
| **---** | **--- PRIMER LOOP ---** | **---** | **---** |
| 7.1 | Aplicar a cada uno (filas Excel) | Control | Loop 1 |
| 7.2 | Condición (`Plan de Prueba Y Periodo tienen valor`) | Control | Loop 1 |
| 7.3 | **Establecer variable** (`FechaPeriodo`) | Variable | Loop 1 |
| 7.4 | **Obtener metadatos de archivo** (ruta de carpeta) | OneDrive | Loop 1 |
| 7.5 | **Mostrar los archivos de la carpeta** (usando identificador) | OneDrive | Loop 1 |
| 7.6 | Condición (`@not(empty(body(...)['value'])) es igual a true`) | Control | Loop 1 |
| **---** | **--- FOR EACH (archivos encontrados) ---** | **---** | **---** |
| 7.7 | **Aplicar a cada uno** (body/value de archivos) | Control | Loop 1.1 |
| 7.7.1 | **Crear un vínculo para compartir** (con Id del archivo) | OneDrive | Loop 1.1 |
| 7.7.2 | **Anexar a variable** (`ArrayPlanes`: NameNoExt + URL web) | Variable | Loop 1.1 |
| **---** | **--- SEGUNDO LOOP ---** | **---** | **---** |
| 8.1 | Aplicar a cada uno (ArrayPlanes) | Control | Loop 2 |
| 8.2 | **Obtener contenido del archivo** | OneDrive | Loop 2 |
| 8.3 | **Actualizar archivo** (con replace) | OneDrive | Loop 2 |
| **---** | **--- ENVÍO DE CORREO ---** | **---** | **---** |
| 9.1 | **Enviar correo** (1 vez, HTML con firma web) | Outlook | Fuera |

---

## Solución de Problemas

### Error: "No se encontró el archivo"

- Verificar que la ruta en OneDrive sea correcta: `/{AÑO}/{MES}/`
- Verificar que el nombre del archivo coincida exactamente con el del Excel
- Verificar que el archivo tenga extensión .pdf en OneDrive

### Error: "No se puede crear enlace"

- Verificar que "Anyone with the link" esté habilitado en el admin center
- Verificar permisos de la cuenta que ejecuta el flow

### Error: "El placeholder no se reemplaza"

- Verificar que el placeholder tenga el formato exacto: `{{PLAN:NOMBRE_ARCHIVO}}`
- Verificar que no haya espacios adicionales o caracteres especiales

### Error: "Compose no disponible"

- Este flujo NO usa acciones Compose
- Usa expresiones directamente en los campos de configuración
- Usa fx para insertar expresiones

### Error: "Expresión con error"

- Usa `concat()` en lugar de corchetes anidados
- Ejemplo: `@{concat(formatDateTime(...),'/',variables(...)[...])}`
- Usa Dynamic Content en lugar de expresiones complejas
- Para la condición 6.6, usa: `@not(empty(body('Mostrar_los_archivos_de_la_carpeta')?['value']))`

### Error: "The datetime string must match ISO 8601 format"

**Causa:** El campo `Periodo` en el Excel contiene un número serial de Excel (ej: `46204`) en lugar de una fecha.

**Solución:** Usar `Establecer variable` con `addDays('1899-12-30', int(numero_serial))` para convertir el número a fecha.

**Pasos:**
1. Inicializar variable `FechaPeriodo` (vacía) ANTES del loop
2. Dentro del loop, usar `Establecer variable FechaPeriodo` con:
```
@{formatDateTime(addDays('1899-12-30', int(items('Aplicar_a_cada_uno')?['Periodo']), 'yyyy-MM-dd'), 'yyyy-MM-dd')}
```
3. Usar `variables('FechaPeriodo')` en la expresión de la carpeta

**Explicación:**
- Excel almacena fechas como números seriales (1 = 01/01/1900)
- `46204` = 26/07/2026
- `addDays('1899-12-30', 46204)` = 26/07/2026
- `formatDateTime(..., 'yyyy-MM-dd')` **fuerza** el formato ISO

---

### Error: "property 'July 1' doesn't exist"

**Causa:** La variable `FechaPeriodo` tiene formato legible ("July 1") en lugar de ISO ("2026-07-01").

**Solución:** Agregar `formatDateTime(..., 'yyyy-MM-dd')` al final de la expresión:
```
@{formatDateTime(addDays('1899-12-30', int(items('Aplicar_a_cada_uno')?['Periodo']), 'yyyy-MM-dd'), 'yyyy-MM-dd')}
```

**Nota:** Sin el `formatDateTime` final, Power Automate convierte la fecha a formato legible ("July 1, 2026") que no se puede usar como key del objeto `MesesEspanol`.

---

### Error: "The value cannot be converted to the target type"

**Causa:** El campo `Periodo` es null o está vacío para algunas filas.

**Solución:** Agregar condición para verificar que AMBOS campos tengan valor.

**Condición:**
```
@and(not(empty(items('Aplicar_a_cada_uno')?['Plan de Prueba'])), not(empty(items('Aplicar_a_cada_uno')?['Periodo'])))
```

---

### Error: Variable cannot be nested in Apply to each

**Causa:** Las variables NO se pueden inicializar dentro de un loop.

**Solución:**
1. Inicializar variables ANTES del loop
2. Usar `Establecer variable` dentro del loop para actualizar valores

---

### Error en Condición 6.6

- **Solución:** Usa la expresión fx:
  ```
  @not(empty(body('Mostrar_los_archivos_de_la_carpeta')?['value']))
  ```
  Y configura la condición como `es igual a` `true`
