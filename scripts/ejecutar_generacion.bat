@echo off
rem ============================================================
rem  PMO-Creasys - Generacion automatica de reporte y plantillas
rem  Copia Excel a temporal para evitar bloqueo OneDrive/Excel
rem  Uso: llamado por Task Scheduler (Mar/Vie/Mie 16:00, hora Chile)
rem  Log: logs\ejecucion_YYYYMMDD.log
rem ============================================================
cd /d C:\Users\progr\PMO-Creasys
set PY=C:\Users\progr\AppData\Local\Python\pythoncore-3.14-64\python.exe
set LOGDIR=C:\Users\progr\PMO-Creasys\logs
mkdir "%LOGDIR%" 2>nul
set LOG=%LOGDIR%\ejecucion_%date:~6,4%%date:~3,2%%date:~0,2%.log

set SRC=C:\Users\progr\OneDrive - CREASYS S.A\Gesti?n Nevasa\Gesti?n y Revisi?n\Seguimiento Requerimientos NevasaCB.xlsx
set DST=%TEMP%\seguimiento_temp.xlsx

echo [%date% %time%] Inicio generacion automatica >> "%LOG%"
echo [%date% %time%] Copiando Excel a temporal para evitar bloqueo... >> "%LOG%"
copy /Y "%SRC%" "%DST%" >> "%LOG%" 2>&1
if errorlevel 1 (
  echo [%date% %time%] ADVERTENCIA: No se pudo copiar el Excel (puede estar abierto). Se intentara leer desde origen. >> "%LOG%"
)

echo [%date% %time%] Ejecutando reporte y plantillas con copia temporal... >> "%LOG%"
"%PY%" -c "import sys;sys.path.insert(0,r'scripts');import generar_reporte_nevasa as g, generar_plantillascorreo as gp, config.rutas as r;tmp=r'%DST%';r.ARCHIVO_FUENTE=tmp;g.ARCHIVO_FUENTE=tmp;gp.ARCHIVO_FUENTE=tmp;g.main();gp.main()" >> "%LOG%" 2>&1
if errorlevel 1 (
  echo [%date% %time%] ERROR en generacion. Revise log. >> "%LOG%"
  exit /b 1
)

echo [%date% %time%] Generacion OK >> "%LOG%"
exit /b 0
