@echo off
title XONIMET 2026 - Extractor Universal de Metadatos
color 0A

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
echo Iniciando XONIMET...
echo.
echo [INFO] Extractor de metadatos para archivos, fotos, audio, video
echo [INFO] Analiza: Imagenes | Audio | Video | PDF | DOCX | XLSX | PPTX
echo [INFO] Genera reportes en PDF y JSON
echo.
echo Modos de uso:
echo   - Interactivo: Arrastra un archivo o escribe su ruta
echo   - Directo:     xonimet.exe "ruta\archivo.jpg"
echo   - JSON:        xonimet.exe "archivo.jpg" --json
echo   - PDF:         xonimet.exe "video.mp4" --pdf
echo.
echo Presiona Ctrl+C para detener
echo ============================================================
echo.

python start.py %*

pause
