#!/usr/bin/env python3
"""
Xonimet - Extractor Universal de Metadatos
Extrae metadatos de archivos, fotos, audio, video, documentos y más.
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

class Xonimet:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
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
        """Extrae metadatos de imágenes"""
        metadata = {}
        try:
            # Usando PIL
            img = Image.open(self.file_path)
            metadata.update({
                'dimensiones': f"{img.width} x {img.height}",
                'modo': img.mode,
                'formato': img.format,
                'info_básica': {
                    'ancho': img.width,
                    'alto': img.height,
                    'proporción': round(img.width / img.height, 2)
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
            
            # Usando exifread para más detalles
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
                metadata['duración_segundos'] = audio.info.length
                metadata['duración_formateado'] = str(datetime.timedelta(seconds=int(audio.info.length)))
                
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
        """Extrae metadatos de videos usando ffmpeg"""
        metadata = {}
        try:
            probe = ffmpeg.probe(str(self.file_path))
            
            # Información del formato
            if 'format' in probe:
                fmt = probe['format']
                metadata['formato'] = {
                    'nombre': fmt.get('format_name'),
                    'duración': fmt.get('duration'),
                    'bitrate': fmt.get('bit_rate'),
                    'tamaño': fmt.get('size'),
                    'tags': fmt.get('tags', {})
                }
            
            # Información de streams
            streams = []
            for stream in probe.get('streams', []):
                stream_info = {
                    'tipo': stream.get('codec_type'),
                    'codec': stream.get('codec_name'),
                    'perfil': stream.get('profile')
                }
                
                if stream['codec_type'] == 'video':
                    stream_info.update({
                        'resolución': f"{stream.get('width')}x{stream.get('height')}",
                        'fps': eval(stream.get('r_frame_rate', '0/1')),
                        'píxeles': stream.get('pix_fmt')
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
                'páginas': len(pdf.pages),
                'encriptado': pdf.is_encrypted,
                'metadatos': pdf.metadata if pdf.metadata else {}
            })
            
            # Extraer texto de la primera página como muestra
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
                'fecha_modificación': core_props.modified,
                'título': core_props.title,
                'asunto': core_props.subject,
                'palabras_clave': core_props.keywords,
                'categoría': core_props.category,
                'comentarios': core_props.comments,
                'párrafos': len(doc.paragraphs),
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
                    'título': wb.properties.title
                }
            })
            
            # Información por hoja
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
                'título': core_props.title,
                'asunto': core_props.subject
            })
            
            # Estadísticas de diapositivas
            slide_stats = {'texto': 0, 'imágenes': 0, 'tablas': 0, 'gráficos': 0}
            for slide in prs.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        slide_stats['texto'] += 1
                    if hasattr(shape, 'image'):
                        slide_stats['imágenes'] += 1
                    if shape.has_table:
                        slide_stats['tablas'] += 1
                    if hasattr(shape, 'chart'):
                        slide_stats['gráficos'] += 1
            metadata['estadísticas_diapositivas'] = slide_stats
            
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_text_metadata(self):
        """Extrae metadatos básicos de archivos de texto"""
        metadata = {}
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                metadata.update({
                    'líneas': len(lines),
                    'palabras': len(content.split()),
                    'caracteres': len(content),
                    'caracteres_sin_espacios': len(content.replace(' ', '').replace('\n', '').replace('\t', '')),
                    'primeras_10_líneas': lines[:10] if len(lines) > 10 else lines
                })
        except Exception as e:
            metadata['error'] = str(e)
        return metadata
    
    def _extract_specific_metadata(self):
        """Determina el tipo de archivo y extrae metadatos específicos"""
        ext = self.file_path.suffix.lower()
        
        # Imágenes
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic']:
            return self._extract_image_metadata()
        
        # Audio
        elif ext in ['.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac', '.wma']:
            return self._extract_audio_metadata()
        
        # Video
        elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']:
            return self._extract_video_metadata()
        
        # PDF
        elif ext == '.pdf':
            return self._extract_pdf_metadata()
        
        # Word
        elif ext in ['.docx', '.doc']:
            return self._extract_docx_metadata()
        
        # Excel
        elif ext in ['.xlsx', '.xls']:
            return self._extract_xlsx_metadata()
        
        # PowerPoint
        elif ext in ['.pptx', '.ppt']:
            return self._extract_pptx_metadata()
        
        # Texto
        elif ext in ['.txt', '.csv', '.json', '.xml', '.html', '.css', '.js', '.py', '.md']:
            return self._extract_text_metadata()
        
        else:
            return {'mensaje': 'Tipo de archivo no soportado para extracción específica'}

def main():
    print("=" * 60)
    print("XONIMET - Extractor Universal de Metadatos")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUso: python xonimet.py <archivo> [--json]")
        print("\nEjemplos:")
        print("  python xonimet.py foto.jpg")
        print("  python xonimet.py documento.pdf --json")
        print("  python xonimet.py video.mp4")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_json = '--json' in sys.argv
    
    if not os.path.exists(file_path):
        print(f"\n❌ Error: El archivo '{file_path}' no existe")
        sys.exit(1)
    
    print(f"\n📁 Procesando: {file_path}")
    print("⏳ Extrayendo metadatos...")
    
    try:
        xonimet = Xonimet(file_path)
        
        if output_json:
            # Salida en JSON
            print(json.dumps(xonimet.metadata, indent=2, ensure_ascii=False, default=str))
        else:
            # Salida formateada
            print("\n" + "=" * 60)
            print("METADATOS DEL ARCHIVO")
            print("=" * 60)
            
            # Info básica
            print("\n📋 INFORMACIÓN BÁSICA:")
            for key, value in xonimet.metadata['archivo'].items():
                if key != 'hashes':
                    print(f"  • {key.replace('_', ' ').title()}: {value}")
            
            # Hashes
            print("\nHASHES:")
            for algo, hash_value in xonimet.metadata['archivo']['hashes'].items():
                print(f"  • {algo.upper()}: {hash_value}")
            
            # Metadatos específicos
            if xonimet.metadata['metadatos_específicos']:
                print("\nMETADATOS ESPECÍFICOS:")
                spec = xonimet.metadata['metadatos_específicos']
                
                if 'error' in spec:
                    print(f"  ⚠️  {spec['error']}")
                else:
                    for key, value in spec.items():
                        if isinstance(value, dict):
                            print(f"\n  📌 {key.replace('_', ' ').title()}:")
                            for subkey, subvalue in value.items():
                                if subvalue:
                                    print(f"    • {subkey}: {subvalue}")
                        else:
                            print(f"  • {key.replace('_', ' ').title()}: {value}")
            
            print("\n" + "=" * 60)
            print("✅ Extracción completada exitosamente")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Error durante la extracción: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
