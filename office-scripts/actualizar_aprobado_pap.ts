/**
 * Office Script: Actualizar Aprobado PaP
 * 
 * Este script automatiza la columna "Aprobado PaP" en la hoja "Seguimiento Nevasa".
 * 
 * Funcionalidad:
 * 1. Para cada fila con estado "Certificación Nevasa":
 *    - Si la columna O está vacía → escribe "Pendiente"
 *    - Si ya tiene un valor → lo mantiene
 * 2. Aplica validación de datos (lista desplegable) a toda la columna O
 * 
 * Valores permitidos: Pendiente, Aprobado, Rechazado
 * 
 * Uso:
 * - Ejecutar manualmente desde Excel Online > Automate > Scripts
 * - Opcionalmente, vincular a un botón en la hoja
 */

function main(workbook: ExcelScript.Workbook) {
  const sheet = workbook.getWorksheet("Seguimiento Nevasa");
  
  if (!sheet) {
    console.error("No se encontró la hoja 'Seguimiento Nevasa'");
    return;
  }

  const usedRange = sheet.getUsedRange();
  
  if (!usedRange) {
    console.error("La hoja está vacía");
    return;
  }

  const rowCount = usedRange.getRowCount();
  const COL_ESTADO = "F";
  const COL_APROBADO_PAP = "O";
  const ESTADO_CERTIFICACION = "Certificación Nevasa";
  const VALOR_POR_DEFECTO = "Pendiente";
  
  let actualizados = 0;
  let mantenidos = 0;

  // Procesar cada fila (asumiendo encabezados en fila 4, datos desde fila 5)
  for (let i = 5; i <= rowCount; i++) {
    const estado = sheet.getRange(`${COL_ESTADO}${i}`).getValue();
    const papCell = sheet.getRange(`${COL_APROBADO_PAP}${i}`);
    
    // Solo procesar si el estado es Certificación Nevasa
    if (estado === ESTADO_CERTIFICACION) {
      const valorActual = papCell.getValue();
      
      if (!valorActual || valorActual === "") {
        // Si está vacío, establecer "Pendiente"
        papCell.setValue(VALOR_POR_DEFECTO);
        actualizados++;
      } else {
        // Si ya tiene valor, mantenerlo
        mantenidos++;
      }
    }
  }

  // Aplicar validación de datos a toda la columna O (desde fila 5 hasta el final)
  const rangoValidacion = sheet.getRange(`${COL_APROBADO_PAP}5:${COL_APROBADO_PAP}${rowCount}`);
  const validacion = rangoValidacion.getDataValidation();
  
  // Configurar regla de lista
  validacion.setRule({
    list: { source: "Pendiente,Aprobado,Rechazado" }
  });
  
  // Configurar mensaje de error
  validacion.setErrorMessage({
    message: "Valor no válido. Use: Pendiente, Aprobado o Rechazado",
    title: "Valor inválido"
  });
  
  // Configurar mensaje de entrada
  validacion.setPrompt({
    message: "Seleccione el estado de aprobación del PaP",
    title: "Aprobado PaP"
  });

  // Aplicar formato a la columna
  const rangoFormato = sheet.getRange(`${COL_APROBADO_PAP}5:${COL_APROBADO_PAP}${rowCount}`);
  rangoFormato.setFormat(
    ExcelScript.RangeFormat.fill,
    { color: "#FFFFFF" }
  );

  console.log(`Proceso completado:`);
  console.log(`- Filas actualizadas (nuevas): ${actualizados}`);
  console.log(`- Filas mantenidas (existentes): ${mantenidos}`);
  console.log(`- Total filas procesadas: ${rowCount - 4}`);
}
