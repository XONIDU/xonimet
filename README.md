# 🔍 XONIMET 2026 - Extractor Universal de Metadatos

**Desarrollado por: Darian Alberto Camacho Salas**  
**SOMOS XONIDU**

---

## ⚠️ ADVERTENCIA

> Solo para fines educativos. Úsalo en archivos propios o con autorización explícita.

---

## 📦 INSTALACIÓN

### Arch Linux (AUR)
```bash
yay -S xonimet
```

### Otros sistemas (Windows, macOS, Linux)
```bash
git clone https://github.com/XONIDU/xonimet.git
cd xonimet
python start.py
```

o

```bash
git clone https://github.com/XONIDU/xonimet.git
cd xonimet
python3 start.py
```

---

### Opción 2 – Comando `xoninstall` (recomendado para futuras herramientas XONI)

Agrega la siguiente función a tu `~/.bashrc` con un solo comando:

```bash
echo 'xoninstall() { if [ -z "$1" ]; then echo "Uso: xoninstall <repo>"; echo "Ej: xoninstall xoniran"; else git clone "https://github.com/XONIDU/$1.git"; fi; }' >> ~/.bashrc && source ~/.bashrc && echo "✅ Listo. Usa: xoninstall xonicli"
```

Luego simplemente escribe:

```bash
xoninstall xonimet
cd xonimet
pip install -r requirements.txt
python start.py
```

> **Nota:** Esta función te servirá para instalar cualquier otra herramienta futura de XONIDU (por ejemplo `xoninstall xonicli`).

---

## 📁 SOLO NECESITAS ESTOS 3 ARCHIVOS

```
xonimet/
├── start.py          # 🟢 EJECUTA ESTE (hace todo)
├── xonimet.py        # 🔵 El programa principal
└── requirements.txt  # 📦 Lista de dependencias
```

---

## 🚀 ASÍ DE FÁCIL: SOLO EJECUTA start.py

El archivo start.py hace TODO automáticamente:

| # | Acción |
|:-:|--------|
| 1 | Detecta Windows, Linux o Mac |
| 2 | Verifica Python instalado |
| 3 | Revisa qué librerías faltan |
| 4 | Las instala automáticamente |
| 5 | Ejecuta el programa |
| 6 | Muestra todos los metadatos |

---

## 🎮 MODOS DE EJECUCIÓN

### Modo Terminal (CLI) - Bajo consumo de recursos
```bash
python xonimet.py 1
```
O simplemente:
```bash
python xonimet.py
```
Y selecciona `[1]` en el menú.

### Modo Gráfico (Web) - Interfaz amigable
```bash
python xonimet.py 2
```
Luego abre tu navegador en: `http://localhost:5000`

---

## 🪟🐧🍎 COMANDOS (para todos los sistemas)

### Modo interactivo (con menú)
```bash
python start.py
python3 start.py
```

### Modo directo (analizar un archivo)
```bash
python start.py foto.jpg
python start.py cancion.mp3
python start.py video.mp4
python start.py documento.pdf
```

### Guardar resultados en JSON
```bash
python start.py imagen.jpg --json
python start.py video.mp4 --json > metadatos.json
```

### Generar reporte PDF
```bash
python start.py foto.jpg --pdf
```

---

## 🪟 ESPECIAL PARA WINDOWS: XONIMET_ADMIN.bat

Si estás en Windows y quieres ejecutar XONIMET con permisos de administrador (recomendado para instalar dependencias automáticamente), usa el archivo `XONIMET_ADMIN.bat`:

```batch
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
```

### ¿Cómo usar XONIMET_ADMIN.bat?

1. **Doble clic** en `XONIMET_ADMIN.bat`
2. Acepta el mensaje de Control de Cuentas de Usuario (UAC)
3. El script instalará automáticamente todas las dependencias
4. XONIMET se iniciará con permisos completos

> **Nota:** Este archivo es especialmente útil si tienes problemas de permisos al instalar dependencias en Windows.

---

## 📂 ARCHIVOS QUE PUEDES ANALIZAR

| Tipo | Formatos | Metadatos extraídos |
|:----:|----------|---------------------|
| 📸 **Fotos** | .jpg, .png, .gif, .bmp, .tiff, .webp | EXIF, GPS, cámara, fecha, dimensiones |
| 🎵 **Audios** | .mp3, .flac, .wav, .ogg, .m4a | Duración, bitrate, artista, álbum, ID3 |
| 🎬 **Videos** | .mp4, .avi, .mov, .mkv, .wmv | Resolución, codecs, fps, streams |
| 📄 **Documentos** | .pdf, .docx, .xlsx, .pptx | Autor, páginas, hojas, estadísticas |
| 📝 **Texto** | .txt, .csv, .json, .py, .html | Líneas, palabras, caracteres |

---

## 🎯 CARACTERÍSTICAS PRINCIPALES

- ✅ **Multiplataforma**: Windows, Linux y macOS
- ✅ **Dos modos de ejecución**: Terminal (CLI) y Gráfico (Web)
- ✅ **Modo terminal**: Bajo consumo de recursos (ideal para equipos antiguos, Raspberry Pi, SSH)
- ✅ **Modo gráfico**: Interfaz web amigable con subida de archivos
- ✅ **Reportes PDF**: Genera informes profesionales
- ✅ **Exportación JSON**: Para integración con otras herramientas
- ✅ **Cálculo de hashes**: MD5, SHA1, SHA256
- ✅ **Soporte Unicode**: Tildes y caracteres especiales
- ✅ **Disponible en AUR**: `yay -S xonimet`

---

## 🔧 PROBLEMAS COMUNES

### ❌ "Python no está instalado"
```bash
# Descarga desde:
https://www.python.org/downloads/
```

### ❌ "externally-managed-environment" en Linux
```bash
# start.py ya lo soluciona automáticamente
# Si quieres manual:
pip install --break-system-packages -r requirements.txt
```

### ❌ "ffmpeg not found" (necesario para videos)
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Arch/Manjaro
sudo pacman -S ffmpeg

# Fedora
sudo dnf install ffmpeg

# macOS
brew install ffmpeg

# Windows
Descarga desde: https://ffmpeg.org/download.html
```

### ❌ "No module named 'reportlab'"
```bash
pip install reportlab
# En Linux con external management:
pip install --break-system-packages reportlab
```

### ❌ "Permisos denegados en Windows"
```bash
# Ejecuta XONIMET_ADMIN.bat como administrador
# O haz clic derecho > "Ejecutar como administrador"
```

### ❌ "'bool' object is not callable" (modo gráfico)
```bash
# Asegúrate de tener la última versión de xonimet.py
# El error ya fue corregido en v3.0
git pull
```

---

## 💡 EJEMPLOS RÁPIDOS

### 1. Ver metadatos de una foto (CLI)
```bash
python xonimet.py 1
# Luego selecciona opción 1 y escribe la ruta
```

### 2. Extraer info de una canción (Web)
```bash
python xonimet.py 2
# Abre http://localhost:5000 y sube tu archivo
```

### 3. Analizar un PDF desde CLI
```bash
python start.py documento.pdf
```

### 4. Generar reporte PDF de un video
```bash
python start.py video.mp4 --pdf
```

---

## ✅ LO QUE PUEDES HACER (Y LO QUE NO)

| ✅ **SÍ** | ❌ **NO** |
|-----------|-----------|
| Analizar tus propios archivos | Usar archivos ajenos sin permiso |
| Aprender sobre metadatos | Fines maliciosos |
| Organizar tu biblioteca multimedia | Modificar archivos originales |
| Compartir el código | Quitar los créditos |
| Generar reportes para tu trabajo | Vender el software |

---

## 📊 EJEMPLO DE SALIDA EN TERMINAL

```
═══════════════════════════════════════════════════════════
METADATOS DEL ARCHIVO
═══════════════════════════════════════════════════════════

INFORMACION BASICA:
  • Nombre: foto.jpg
  • Ruta: /home/usuario/foto.jpg
  • Tamaño Formateado: 2.50 MB
  • Creado: 2026-04-03T15:30:45
  • Extension: .jpg

HASHES:
  • MD5: a1b2c3d4e5f6789012345678
  • SHA256: abc123def456...

METADATOS ESPECIFICOS:
  • Dimensiones: 1920 x 1080
  • Modo: RGB
  • Exif: {'Make': 'Canon', 'Model': 'EOS R6', ...}

═══════════════════════════════════════════════════════════
```

---

## 📞 CONTACTO

| Red | Usuario |
|-----|---------|
| 📸 **Instagram** | @xonidu |
| 📧 **Email** | xonidu@gmail.com |
| 💻 **GitHub** | XONIDU/xonimet |

---

## 📋 REQUISITOS DEL SISTEMA

- **Python**: 3.8 o superior
- **RAM**: 1 GB mínimo (512 MB para funcionamiento básico)
- **Espacio**: 200 MB para dependencias
- **FFmpeg**: Necesario solo para archivos de video

---

## 🛠️ TECNOLOGÍAS UTILIZADAS

- Python 3
- Pillow (Imágenes)
- Mutagen (Audio)
- FFmpeg (Video)
- PyPDF2 (PDF)
- python-docx (Word)
- openpyxl (Excel)
- python-pptx (PowerPoint)
- reportlab (Reportes PDF)
- Flask (Interfaz gráfica)

---

## 📜 LICENCIA

MIT License - Copyright (c) 2026 Darian Alberto Camacho Salas

Ver archivo `Legal` para más detalles.

---

## ⭐ CRÉDITOS

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              XONIMET 2026 - Extractor Universal          ║
║                                                           ║
║         Hecho con ❤️ por Darian Alberto Camacho Salas     ║
║                                                           ║
║         "La información está en los detalles"            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

**XONIDU - Enseñando automatización, construyendo conocimiento**
