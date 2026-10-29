@echo off
setlocal EnableExtensions
chcp 65001 >nul

rem ============================================================
rem  PMO-Creasys - Generacion automatica de reporte y plantillas
rem  Busca Excel en OneDrive y lo copia a temporal
rem  Ejecucion mediante Task Scheduler
rem  Log: logs\ejecucion_YYYYMMDD.log
rem ============================================================

rem ------------------------------------------------------------
rem 1. Configuracion
rem ------------------------------------------------------------

cd /d "C:\Users\progr\PMO-Creasys"
if errorlevel 1 exit /b 1

set "PY=C:\Users\progr\AppData\Local\Python\pythoncore-3.14-64\python.exe"
set "LOGDIR=C:\Users\progr\PMO-Creasys\logs"
set "ONEDRIVE=C:\Users\progr\OneDrive - CREASYS S.A"
set "ARCHIVO=Seguimiento Requerimientos NevasaCB.xlsx"
set "DST=%TEMP%\seguimiento_temp.xlsx"

if not exist "%LOGDIR%" mkdir "%LOGDIR%" 2>nul

rem Fecha para el log, independiente del formato regional de Windows
for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set "FECHA=%%I"

set "LOG=%LOGDIR%\ejecucion_%FECHA%.log"

echo.>> "%LOG%"
echo ============================================================>> "%LOG%"
echo [%date% %time%] Inicio generacion automatica>> "%LOG%"

rem ------------------------------------------------------------
rem 2. Validar Python
rem ------------------------------------------------------------

if not exist "%PY%" (
    echo [%date% %time%] ERROR: No se encontro Python: "%PY%">> "%LOG%"
    exit /b 1
)

rem ------------------------------------------------------------
rem 3. Buscar archivo Excel en OneDrive
rem    PowerShell gestiona correctamente los caracteres Unicode
rem ------------------------------------------------------------

echo [%date% %time%] Buscando archivo Excel en OneDrive...>> "%LOG%"

set "SRC="

for /f "usebackq delims=" %%F in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='SilentlyContinue'; $p = Get-ChildItem -LiteralPath $env:ONEDRIVE -Filter $env:ARCHIVO -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName; if ($p) { [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false); [Console]::WriteLine($p) }"`) do (
    set "SRC=%%F"
)

if not defined SRC (
    echo [%date% %time%] ERROR: No se encontro "%ARCHIVO%" en "%ONEDRIVE%">> "%LOG%"
    echo [%date% %time%] Verifique que OneDrive este sincronizado y que el archivo exista.>> "%LOG%"
    exit /b 1
)

echo [%date% %time%] Archivo encontrado: "%SRC%">> "%LOG%"

rem ------------------------------------------------------------
rem 4. Copiar Excel a temporal
rem ------------------------------------------------------------

echo [%date% %time%] Copiando Excel a temporal...>> "%LOG%"

copy /Y "%SRC%" "%DST%" >> "%LOG%" 2>&1

if errorlevel 1 (
    echo [%date% %time%] ERROR: No se pudo copiar el Excel.>> "%LOG%"
    exit /b 1
)

if not exist "%DST%" (
    echo [%date% %time%] ERROR: No se genero el archivo temporal.>> "%LOG%"
    exit /b 1
)

echo [%date% %time%] Copia temporal generada correctamente.>> "%LOG%"

rem ------------------------------------------------------------
rem 5. Ejecutar reporte y plantillas de correo
rem    Ambos scripts utilizan la copia temporal del Excel
rem ------------------------------------------------------------

echo [%date% %time%] Ejecutando reporte y plantillas...>> "%LOG%"

"%PY%" -c "import sys; sys.path.insert(0, r'scripts'); import generar_reporte_nevasa as g, generar_plantillascorreo as gp, config.rutas as r; tmp=r'%DST%'; r.ARCHIVO_FUENTE=tmp; g.ARCHIVO_FUENTE=tmp; gp.ARCHIVO_FUENTE=tmp; g.main(); gp.main()" >> "%LOG%" 2>&1

if errorlevel 1 (
    echo [%date% %time%] ERROR: Fallo la generacion. Revise el log.>> "%LOG%"
    exit /b 1
)

rem ------------------------------------------------------------
rem 6. Finalizacion
rem ------------------------------------------------------------

echo [%date% %time%] Generacion OK>> "%LOG%"
echo [%date% %time%] Proceso finalizado correctamente.>> "%LOG%"

exit /b 0
