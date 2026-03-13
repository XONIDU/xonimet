#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONIMET 2026 - Extractor Universal de Metadatos (Modo Interactivo)
Extrae metadatos de archivos, fotos, audio, video, documentos y mas.
"""

import os
import sys
import json
import datetime
import hashlib
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
import ffmpeg
from PyPDF2 import PdfReader
import docx
from openpyxl import load_workbook
from pptx import Presentation
import exifread
import warnings
warnings.filterwarnings('ignore')

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'

class Xonimet:
    def __init__(self, file_path=None):
        self.file_path = Path(file_path) if file_path else None
        self.metadata = {}
    
    def set_file(self, file_path):
        """Establece el archivo a analizar"""
        self.file_path = Path(file_path)
        self.metadata = {}
    
    def extract_all(self):
        """Extrae todos los metadatos del archivo"""
        if not self.file_path or not self.file_path.exists():
            return {'error': 'Archivo no existe'}
        
        self.metadata = {
            'archivo': {
                'nombre': self.file_path.name,
                'ruta': str(self.file_path.absolute()),
                'tamaño_bytes': self.file_path.stat().st_size,
                'tamaño_formateado': self._format_bytes(self.file_path.stat().st_size),
                'creado': datetime.datetime.fromtimestamp(self.file_path.stat().st_ctime).isoformat(),
                'modificado': datetime.datetime.fromtimestamp(self.file_path.stat().st_mtime).isoformat(),
                'accedido': datetime.datetime.fromtimestamp(self.file_path.stat().st_atime).isoformat(),
                'extensión': self.file_path.suffix.lower(),
                'tipo_mime': self._get_mime_type(),
                'hashes': self._calculate_hashes()
            },
            'metadatos_específicos': self._extract_specific_metadata()
        }
        return self.metadata
    
    def _format_bytes(self, bytes):
        """Formatea bytes a unidades legibles"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
    
    def _get_mime_type(self):
        """Obtiene el tipo MIME del archivo"""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(str(self.file_path))
        return mime_type or 'desconocido'
    
    def _calculate_hashes(self):
        """Calcula hashes del archivo"""
        hashes = {}
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()
                hashes['md5'] = hashlib.md5(data).hexdigest()
                hashes['sha1'] = hashlib.sha1(data).hexdigest()
                hashes['sha256'] = hashlib.sha256(data).hexdigest()
        except:
            hashes['error'] = 'No se pudo calcular hashes'
        return hashes
    
    def _extract_image_metadata(self):
        """Extrae metadatos de imagenes"""
        metadata = {}
        try:
            img = Image.open(self.file_path)
            metadata.update({
                'dimensiones': f"{img.width} x {img.height}",
                'modo': img.mode,
                'formato': img.format,
                'info_basica': {
                    'ancho': img.width,
                    'alto': img.height,
                    'proporcion': round(img.width / img.height, 2)
                }
            })
            
            # Extraer EXIF
            if hasattr(img, '_getexif') and img._getexif():
                exif = {}
                for tag_id, value in img._getexif().items():
                    tag = TAGS.get(tag_id, tag_id)
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore')
                        except:
                            value = str(value)
                    exif[tag] = str(value)
                metadata['exif'] = exif
            
            # Usando exifread para mas detalles
            with open(self.file_path, 'rb') as f:
                tags = exifread.process_file(f, details=True)
                if tags:
                    metadata['exif_detallado'] = {str(k): str(v) for k, v in tags.items()}
                    
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_audio_metadata(self):
        """Extrae metadatos de archivos de audio"""
        metadata = {}
        try:
            audio = mutagen.File(self.file_path)
            if audio:
                metadata['formato'] = type(audio).__name__
                metadata['duracion_segundos'] = audio.info.length
                metadata['duracion_formateado'] = str(datetime.timedelta(seconds=int(audio.info.length)))
                
                if hasattr(audio.info, 'bitrate'):
                    metadata['bitrate'] = f"{audio.info.bitrate // 1000} kbps"
                
                if hasattr(audio.info, 'sample_rate'):
                    metadata['frecuencia_muestreo'] = f"{audio.info.sample_rate} Hz"
                
                # Tags/metadatos
                if hasattr(audio, 'tags') and audio.tags:
                    tags = {}
                    for key, value in audio.tags.items():
                        if value:
                            tags[key] = str(value[0]) if isinstance(value, list) else str(value)
                    metadata['etiquetas'] = tags
                    
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_video_metadata(self):
        """Extrae metadatos de videos"""
        metadata = {}
        try:
            probe = ffmpeg.probe(str(self.file_path))
            
            if 'format' in probe:
                fmt = probe['format']
                metadata['formato'] = {
                    'nombre': fmt.get('format_name'),
                    'duracion': fmt.get('duration'),
                    'bitrate': fmt.get('bit_rate'),
                    'tamaño': fmt.get('size'),
                    'tags': fmt.get('tags', {})
                }
            
            streams = []
            for stream in probe.get('streams', []):
                stream_info = {
                    'tipo': stream.get('codec_type'),
                    'codec': stream.get('codec_name'),
                    'perfil': stream.get('profile')
                }
                
                if stream['codec_type'] == 'video':
                    stream_info.update({
                        'resolucion': f"{stream.get('width')}x{stream.get('height')}",
                        'fps': eval(stream.get('r_frame_rate', '0/1')),
                        'pixeles': stream.get('pix_fmt')
                    })
                elif stream['codec_type'] == 'audio':
                    stream_info.update({
                        'canales': stream.get('channels'),
                        'frecuencia': stream.get('sample_rate')
                    })
                
                streams.append(stream_info)
            
            metadata['streams'] = streams
            
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_pdf_metadata(self):
        """Extrae metadatos de PDFs"""
        metadata = {}
        try:
            pdf = PdfReader(self.file_path)
            metadata.update({
                'paginas': len(pdf.pages),
                'encriptado': pdf.is_encrypted,
                'metadatos': dict(pdf.metadata) if pdf.metadata else {}
            })
            
            if len(pdf.pages) > 0:
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                metadata['primeras_palabras'] = text[:200] + '...' if len(text) > 200 else text
                
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_docx_metadata(self):
        """Extrae metadatos de documentos Word"""
        metadata = {}
        try:
            doc = docx.Document(self.file_path)
            core_props = doc.core_properties
            metadata.update({
                'autor': core_props.author,
                'creador': core_props.created,
                'modificado_por': core_props.last_modified_by,
                'fecha_modificacion': core_props.modified,
                'titulo': core_props.title,
                'asunto': core_props.subject,
                'palabras_clave': core_props.keywords,
                'categoria': core_props.category,
                'comentarios': core_props.comments,
                'parrafos': len(doc.paragraphs),
                'tablas': len(doc.tables)
            })
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_xlsx_metadata(self):
        """Extrae metadatos de Excel"""
        metadata = {}
        try:
            wb = load_workbook(self.file_path, data_only=True)
            metadata.update({
                'hojas': wb.sheetnames,
                'hojas_activas': len(wb.sheetnames),
                'propiedades': {
                    'creador': wb.properties.creator,
                    'creado': str(wb.properties.created) if wb.properties.created else None,
                    'modificado': str(wb.properties.modified) if wb.properties.modified else None,
                    'titulo': wb.properties.title
                }
            })
            
            sheets_info = {}
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                sheets_info[sheet_name] = {
                    'filas': sheet.max_row,
                    'columnas': sheet.max_column,
                    'celdas_con_datos': sum(1 for row in sheet.iter_rows() for cell in row if cell.value)
                }
            metadata['detalle_hojas'] = sheets_info
            
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_pptx_metadata(self):
        """Extrae metadatos de PowerPoint"""
        metadata = {}
        try:
            prs = Presentation(self.file_path)
            core_props = prs.core_properties
            metadata.update({
                'diapositivas': len(prs.slides),
                'autor': core_props.author,
                'creado': str(core_props.created) if core_props.created else None,
                'modificado': str(core_props.modified) if core_props.modified else None,
                'titulo': core_props.title,
                'asunto': core_props.subject
            })
            
            slide_stats = {'texto': 0, 'imagenes': 0, 'tablas': 0, 'graficos': 0}
            for slide in prs.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        slide_stats['texto'] += 1
                    if hasattr(shape, 'image'):
                        slide_stats['imagenes'] += 1
                    if shape.has_table:
                        slide_stats['tablas'] += 1
                    if hasattr(shape, 'chart'):
                        slide_stats['graficos'] += 1
            metadata['estadisticas_diapositivas'] = slide_stats
            
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_text_metadata(self):
        """Extrae metadatos basicos de archivos de texto"""
        metadata = {}
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                metadata.update({
                    'lineas': len(lines),
                    'palabras': len(content.split()),
                    'caracteres': len(content),
                    'caracteres_sin_espacios': len(content.replace(' ', '').replace('\n', '').replace('\t', '')),
                    'primeras_10_lineas': lines[:10] if len(lines) > 10 else lines
                })
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_specific_metadata(self):
        """Determina el tipo de archivo y extrae metadatos especificos"""
        ext = self.file_path.suffix.lower()
        
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic']:
            return self._extract_image_metadata()
        elif ext in ['.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac', '.wma']:
            return self._extract_audio_metadata()
        elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']:
            return self._extract_video_metadata()
        elif ext == '.pdf':
            return self._extract_pdf_metadata()
        elif ext in ['.docx', '.doc']:
            return self._extract_docx_metadata()
        elif ext in ['.xlsx', '.xls']:
            return self._extract_xlsx_metadata()
        elif ext in ['.pptx', '.ppt']:
            return self._extract_pptx_metadata()
        elif ext in ['.txt', '.csv', '.json', '.xml', '.html', '.css', '.js', '.py', '.md']:
            return self._extract_text_metadata()
        else:
            return {'mensaje': 'Tipo de archivo no soportado para extraccion especifica'}
    
    def print_metadata(self, metadata=None):
        """Imprime los metadatos de forma formateada"""
        if metadata is None:
            metadata = self.metadata
        
        if not metadata:
            print(f"{Colors.RED}No hay metadatos para mostrar{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}METADATOS DEL ARCHIVO{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════{Colors.END}")
        
        # Info basica
        print(f"\n{Colors.GREEN}{Colors.BOLD}INFORMACION BASICA:{Colors.END}")
        archivo = metadata.get('archivo', {})
        for key, value in archivo.items():
            if key != 'hashes':
                print(f"  {Colors.YELLOW}•{Colors.END} {key.replace('_', ' ').title()}: {value}")
        
        # Hashes
        if 'hashes' in archivo:
            print(f"\n{Colors.GREEN}{Colors.BOLD}HASHES:{Colors.END}")
            for algo, hash_value in archivo['hashes'].items():
                print(f"  {Colors.YELLOW}•{Colors.END} {algo.upper()}: {hash_value}")
        
        # Metadatos especificos
        if 'metadatos_específicos' in metadata and metadata['metadatos_específicos']:
            print(f"\n{Colors.GREEN}{Colors.BOLD}METADATOS ESPECIFICOS:{Colors.END}")
            spec = metadata['metadatos_específicos']
            
            if 'error' in spec:
                print(f"  {Colors.RED}⚠  {spec['error']}{Colors.END}")
            else:
                for key, value in spec.items():
                    if isinstance(value, dict):
                        print(f"\n  {Colors.CYAN}• {key.replace('_', ' ').title()}:{Colors.END}")
                        for subkey, subvalue in value.items():
                            if subvalue:
                                print(f"    {Colors.YELLOW}•{Colors.END} {subkey}: {subvalue}")
                    else:
                        print(f"  {Colors.YELLOW}•{Colors.END} {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════{Colors.END}")

def clear_screen():
    """Limpia la pantalla segun el sistema"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Muestra el menu principal"""
    menu = f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════
                   XONIMET 2026 v1.0                    
              Extractor Universal de Metadatos           
                    MODO INTERACTIVO                      
═══════════════════════════════════════════════════════════{Colors.END}

{Colors.GREEN}ARCHIVOS SOPORTADOS:{Colors.END}
  Imagenes | Audio | Video | PDF/DOCS | Texto

{Colors.YELLOW}═══════════════════════════════════════════════════════════{Colors.END}

{Colors.BOLD}MENU PRINCIPAL:{Colors.END}
  {Colors.CYAN}[1]{Colors.END} Seleccionar archivo para analizar
  {Colors.CYAN}[2]{Colors.END} Analizar archivo actual
  {Colors.CYAN}[3]{Colors.END} Guardar resultados en JSON
  {Colors.CYAN}[4]{Colors.END} Ver informacion del archivo actual
  {Colors.CYAN}[5]{Colors.END} Cambiar archivo
  {Colors.CYAN}[6]{Colors.END} Ayuda / Formatos soportados
  {Colors.CYAN}[7]{Colors.END} Limpiar pantalla
  {Colors.CYAN}[0]{Colors.END} Salir

{Colors.YELLOW}═══════════════════════════════════════════════════════════{Colors.END}
"""
    print(menu)

def print_help():
    """Muestra ayuda detallada"""
    help_text = f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════
AYUDA - FORMATOS SOPORTADOS
═══════════════════════════════════════════════════════════{Colors.END}

{Colors.GREEN}IMAGENES:{Colors.END}
  • .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .heic
  {Colors.YELLOW}→{Colors.END} EXIF, dimensiones, GPS, modelo camara, fecha

{Colors.GREEN}AUDIO:{Colors.END}
  • .mp3, .flac, .wav, .ogg, .m4a, .aac, .wma
  {Colors.YELLOW}→{Colors.END} Duracion, bitrate, etiquetas ID3, artista, album

{Colors.GREEN}VIDEO:{Colors.END}
  • .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm
  {Colors.YELLOW}→{Colors.END} Resolucion, codecs, fps, streams

{Colors.GREEN}DOCUMENTOS:{Colors.END}
  • .pdf: paginas, autor, titulo, metadatos
  • .docx, .doc: autor, fechas, estadisticas
  • .xlsx, .xls: hojas, celdas, propiedades
  • .pptx, .ppt: diapositivas, estadisticas

{Colors.GREEN}TEXTO:{Colors.END}
  • .txt, .csv, .json, .xml, .html, .css, .js, .py, .md
  {Colors.YELLOW}→{Colors.END} Lineas, palabras, caracteres

{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════{Colors.END}
"""
    print(help_text)

def select_file():
    """Selecciona un archivo interactivamente"""
    print(f"\n{Colors.CYAN}SELECCIONAR ARCHIVO{Colors.END}")
    print(f"{Colors.YELLOW}Escribe la ruta del archivo (o 'cancel' para volver):{Colors.END}")
    
    while True:
        file_path = input(f"{Colors.GREEN}→{Colors.END} ").strip()
        
        if file_path.lower() == 'cancel':
            return None
        
        if not file_path:
            continue
        
        # Expandir ~ si es necesario
        file_path = os.path.expanduser(file_path)
        
        if os.path.exists(file_path):
            return file_path
        else:
            print(f"{Colors.RED}El archivo no existe. Intenta de nuevo:{Colors.END}")

def save_to_json(metadata):
    """Guarda los metadatos en un archivo JSON"""
    if not metadata:
        print(f"{Colors.RED}No hay metadatos para guardar{Colors.END}")
        return
    
    # Crear nombre de archivo basado en el original
    original_name = metadata.get('archivo', {}).get('nombre', 'desconocido')
    json_name = f"{Path(original_name).stem}_metadatos.json"
    
    try:
        with open(json_name, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)
        print(f"{Colors.GREEN}Metadatos guardados en: {json_name}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error guardando: {e}{Colors.END}")

def main():
    """Funcion principal del modo interactivo"""
    xonimet = Xonimet()
    current_file = None
    
    while True:
        clear_screen()
        print_menu()
        
        # Mostrar archivo actual si existe
        if current_file:
            print(f"{Colors.GREEN}Archivo actual: {current_file}{Colors.END}")
        else:
            print(f"{Colors.YELLOW}Ningun archivo seleccionado{Colors.END}")
        
        opcion = input(f"\n{Colors.BOLD}Selecciona una opcion [0-7]:{Colors.END} ").strip()
        
        if opcion == '1' or opcion == '5':  # Seleccionar/cambiar archivo
            new_file = select_file()
            if new_file:
                current_file = new_file
                xonimet.set_file(current_file)
                print(f"{Colors.GREEN}Archivo seleccionado: {current_file}{Colors.END}")
                input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")
        
        elif opcion == '2':  # Analizar archivo actual
            if not current_file:
                print(f"{Colors.RED}Primero selecciona un archivo (opcion 1){Colors.END}")
                input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")
                continue
            
            print(f"\n{Colors.CYAN}Analizando archivo...{Colors.END}")
            metadata = xonimet.extract_all()
            clear_screen()
            xonimet.print_metadata(metadata)
            input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")
        
        elif opcion == '3':  # Guardar en JSON
            if not xonimet.metadata:
                print(f"{Colors.RED}Primero analiza un archivo (opcion 2){Colors.END}")
                input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")
                continue
            
            save_to_json(xonimet.metadata)
            input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")
        
        elif opcion == '4':  # Ver informacion del archivo actual
            if not current_file:
                print(f"{Colors.RED}No hay archivo seleccionado{Colors.END}")
            else:
                print(f"\n{Colors.CYAN}Informacion del archivo actual:{Colors.END}")
                print(f"  {Colors.YELLOW}•{Colors.END} Ruta: {current_file}")
                print(f"  {Colors.YELLOW}•{Colors.END} Tamaño: {xonimet._format_bytes(os.path.getsize(current_file))}")
                print(f"  {Colors.YELLOW}•{Colors.END} Extension: {Path(current_file).suffix}")
            input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")
        
        elif opcion == '6':  # Ayuda
            clear_screen()
            print_help()
            input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")
        
        elif opcion == '7':  # Limpiar pantalla
            clear_screen()
        
        elif opcion == '0':  # Salir
            print(f"\n{Colors.GREEN}Gracias por usar XONIMET 2026!{Colors.END}")
            print(f"{Colors.CYAN}Desarrollado por Darian Alberto Camacho Salas{Colors.END}")
            break
        
        else:
            print(f"{Colors.RED}Opcion no valida. Intenta de nuevo.{Colors.END}")
            input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")

if __name__ == "__main__":
    try:
        # Si hay argumentos de linea de comandos, usarlos
        if len(sys.argv) > 1 and sys.argv[1] not in ['-h', '--help']:
            file_path = sys.argv[1]
            if os.path.exists(file_path):
                xonimet = Xonimet(file_path)
                metadata = xonimet.extract_all()
                
                if '--json' in sys.argv:
                    print(json.dumps(metadata, indent=2, ensure_ascii=False, default=str))
                else:
                    xonimet.print_metadata(metadata)
            else:
                print(f"{Colors.RED}El archivo '{file_path}' no existe{Colors.END}")
        else:
            # Modo interactivo
            main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Hasta pronto!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
