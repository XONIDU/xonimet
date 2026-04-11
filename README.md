# 🔍 XONIMET 2026 - Extractor Universal de Metadatos

**Desarrollado por: Darian Alberto Camacho Salas**

SOMOS XONIDU
---

## ⚠️ ADVERTENCIA

> **Solo para fines educativos. Úsalo en archivos propios o con autorización explícita.**

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

**El archivo start.py hace TODO automáticamente:**

| # | Acción |
|:-:|--------|
| 1 | Detecta Windows, Linux o Mac |
| 2 | Verifica Python instalado |
| 3 | Revisa qué librerías faltan |
| 4 | Las instala automáticamente |
| 5 | Ejecuta el programa |
| 6 | Muestra todos los metadatos |

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
- ✅ **Modo interactivo**: Menú fácil de usar
- ✅ **Línea de comandos**: Para automatización
- ✅ **Reportes PDF**: Genera informes profesionales
- ✅ **Exportación JSON**: Para integración con otras herramientas
- ✅ **Cálculo de hashes**: MD5, SHA1, SHA256
- ✅ **Soporte Unicode**: Tildes y caracteres especiales

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

---

## 💡 EJEMPLOS RÁPIDOS

### 1. Ver metadatos de una foto
```bash
python start.py vacaciones.jpg
```
*Muestra: modelo de cámara, fecha, GPS, configuración*

### 2. Extraer info de una canción
```bash
python start.py cancion.mp3
```
*Muestra: artista, álbum, duración, bitrate, género*

### 3. Analizar un PDF
```bash
python start.py documento.pdf
```
*Muestra: autor, páginas, fecha creación, metadatos*

### 4. Generar reporte PDF de un video
```bash
python start.py video.mp4 --pdf
```
*Genera un PDF con todos los metadatos del video*

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

---

