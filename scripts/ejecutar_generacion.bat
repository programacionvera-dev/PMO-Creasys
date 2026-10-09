@echo off
rem ============================================================
rem  PMO-Creasys - Generacion automatica de reporte y plantillas
rem  Ejecuta: generar_reporte_nevasa.py + generar_plantillascorreo.py
rem  Uso: llamado por Task Scheduler (Mar/Vie/Mie 16:00, hora Chile)
rem  Log: logs\ejecucion_YYYYMMDD.log
rem ============================================================
cd /d C:\Users\progr\PMO-Creasys
set PY=C:\Users\progr\AppData\Local\Python\pythoncore-3.14-64\python.exe
set LOGDIR=C:\Users\progr\PMO-Creasys\logs
mkdir "%LOGDIR%" 2>nul
set LOG=%LOGDIR%\ejecucion_%date:~6,4%%date:~3,2%%date:~0,2%.log

echo [%date% %time%] Inicio generacion automatica >> "%LOG%"

echo [%date% %time%] Ejecutando generar_reporte_nevasa.py... >> "%LOG%"
"%PY%" scripts\generar_reporte_nevasa.py >> "%LOG%" 2>&1
if errorlevel 1 (
  echo [%date% %time%] ERROR en generar_reporte_nevasa.py. Revise que el Excel de seguimiento este cerrado. >> "%LOG%"
  exit /b 1
)

echo [%date% %time%] Ejecutando generar_plantillascorreo.py... >> "%LOG%"
"%PY%" scripts\generar_plantillascorreo.py >> "%LOG%" 2>&1
if errorlevel 1 (
  echo [%date% %time%] ERROR en generar_plantillascorreo.py. >> "%LOG%"
  exit /b 1
)

echo [%date% %time%] Generacion OK >> "%LOG%"
exit /b 0
