@echo off
title XONIMET 2026 - Extractor Universal de Metadatos
color 0A

:: ============================================================
:: IR AL DIRECTORIO DONDE ESTA EL SCRIPT .BAT
:: ============================================================
cd /d "%~dp0"

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR
:: ============================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    echo.
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: ============================================================
:: VERIFICAR QUE start.py EXISTE
:: ============================================================
if not exist "%~dp0start.py" (
    echo [ERROR] No se encuentra start.py en esta carpeta
    echo.
    echo Ruta actual: %~dp0
    echo.
    echo Asegurate de que start.py esta en la misma carpeta que este .bat
    echo.
    pause
    exit /B
)

:: ============================================================
:: VERIFICAR QUE xonimet.py EXISTE
:: ============================================================
if not exist "%~dp0xonimet.py" (
    echo [ERROR] No se encuentra xonimet.py en esta carpeta
    echo.
    echo Ruta actual: %~dp0
    echo.
    echo Asegurate de que xonimet.py esta en la misma carpeta que este .bat
    echo.
    pause
    exit /B
)

:: ============================================================
:: EJECUTAR start.py CON PERMISOS DE ADMINISTRADOR
:: ============================================================
cls
echo ============================================================
echo           XONIMET 2026 - Extractor Universal
echo              (Modo Administrador)
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo.
echo [INFO] Directorio de trabajo: %~dp0
echo.
echo Iniciando XONIMET...
echo.
echo [INFO] Extractor de metadatos para archivos, fotos, audio, video
echo [INFO] Analiza: Imagenes ^| Audio ^| Video ^| PDF ^| DOCX ^| XLSX ^| PPTX
echo [INFO] Genera reportes en PDF y JSON
echo.
echo [INFO] Modos de ejecucion:
echo   - Terminal (CLI)  : Bajo consumo de recursos
echo   - Grafico (Web)   : Interfaz en http://localhost:5000
echo.
echo Presiona Ctrl+C para detener
echo ============================================================
echo.

python start.py %*

pause