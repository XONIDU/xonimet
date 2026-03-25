#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONIMET 2026 - Lanzador Universal de Extractor de Metadatos
Este script ejecuta xonimet.py y verifica las dependencias
Desarrollado por: Darian Alberto Camacho Salas
SOMOS XONIDU
"""

import subprocess
import sys
import os
import platform
import shutil
import importlib.util

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        """Verifica si la terminal soporta colores"""
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

# Desactivar colores si no hay soporte
if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

def get_system():
    """Detecta el sistema operativo"""
    return platform.system().lower()

def get_linux_distro():
    """Detecta la distribucion de Linux"""
    if get_system() != 'linux':
        return None
    
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content:
                    return 'ubuntu'
                elif 'debian' in content:
                    return 'debian'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content:
                    return 'centos'
                elif 'arch' in content:
                    return 'arch'
                elif 'manjaro' in content:
                    return 'manjaro'
                elif 'mint' in content:
                    return 'mint'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    """Obtiene el comando Python correcto"""
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def print_banner():
    """Muestra el banner de XONIMET"""
    sistema = get_system()
    distro = get_linux_distro()
    
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.BLUE}{Colors.BOLD}═══════════════════════════════════════════════════════════
                    XONIMET 2026 v1.0                    
              Extractor Universal de Metadatos            
              Extrae informacion de: Fotos, Audio,        
              Video, Documentos y mas                     
                                                          
              Sistema detectado: {sistema_texto}            
                                                          
              Desarrollado por: Darian Alberto            
              Camacho Salas                               
═══════════════════════════════════════════════════════════{Colors.END}
    """
    print(banner)

def check_python():
    """Verifica Python instalado"""
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_command(comando):
    """Verifica si un comando existe"""
    return shutil.which(comando) is not None

def check_python_module(module_name):
    """Verifica si un modulo de Python esta instalado"""
    return importlib.util.find_spec(module_name) is not None

def check_dependencies():
    """Verifica todas las dependencias de Python necesarias"""
    print(f"\n{Colors.BOLD}Verificando dependencias de Python...{Colors.END}")
    
    dependencias = [
        ('Pillow', 'pillow', 'Imagenes', 'PIL'),
        ('mutagen', 'mutagen', 'Audio', 'mutagen'),
        ('ffmpeg', 'ffmpeg-python', 'Video', 'ffmpeg'),
        ('PyPDF2', 'pypdf2', 'PDF', 'PyPDF2'),
        ('docx', 'python-docx', 'Word', 'docx'),
        ('openpyxl', 'openpyxl', 'Excel', 'openpyxl'),
        ('pptx', 'python-pptx', 'PowerPoint', 'pptx'),
        ('exifread', 'exifread', 'EXIF', 'exifread')
    ]
    
    faltantes = []
    
    for modulo, paquete, desc, import_name in dependencias:
        if check_python_module(import_name):
            print(f"{Colors.GREEN}  - {modulo} ({desc}): OK{Colors.END}")
        else:
            print(f"{Colors.YELLOW}  - {modulo} ({desc}): FALTANTE{Colors.END}")
            faltantes.append(paquete)
    
    # Verificar FFmpeg del sistema
    if not check_command('ffmpeg'):
        print(f"{Colors.YELLOW}  - FFmpeg (sistema): FALTANTE (necesario para videos){Colors.END}")
        faltantes.append('ffmpeg-sistema')
    else:
        print(f"{Colors.GREEN}  - FFmpeg (sistema): OK{Colors.END}")
    
    return faltantes

def install_dependencies(faltantes):
    """Instala las dependencias faltantes"""
    if not faltantes:
        return True
    
    print(f"\n{Colors.BOLD}Instalando dependencias faltantes...{Colors.END}")
    
    sistema = get_system()
    distro = get_linux_distro()
    
    # Separar paquetes Python de FFmpeg
    python_paquetes = [p for p in faltantes if p != 'ffmpeg-sistema']
    ffmpeg_falta = 'ffmpeg-sistema' in faltantes
    
    # Instalar paquetes Python
    if python_paquetes:
        print(f"Paquetes Python a instalar: {', '.join(python_paquetes)}")
        
        # Construir comando de instalacion
        cmd = [sys.executable, '-m', 'pip', 'install']
        
        # Agregar opciones segun sistema
        if sistema == 'linux':
            if distro in ['arch', 'manjaro', 'fedora']:
                cmd.append('--break-system-packages')
                print(f"{Colors.YELLOW}Usando --break-system-packages para {distro}{Colors.END}")
            else:
                cmd.append('--user')
        elif sistema == 'darwin':
            cmd.append('--user')
        
        cmd.extend(python_paquetes)
        
        # Intentar instalacion
        try:
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}Dependencias de Python instaladas correctamente{Colors.END}")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}Error instalando dependencias: {e}{Colors.END}")
            print(f"\n{Colors.YELLOW}Intentando metodo alternativo...{Colors.END}")
            
            # Segundo intento: solo --user
            try:
                cmd2 = [sys.executable, '-m', 'pip', 'install', '--user'] + python_paquetes
                subprocess.run(cmd2, check=True)
                print(f"{Colors.GREEN}Instaladas con --user{Colors.END}")
            except:
                print(f"{Colors.RED}Fallo la instalacion{Colors.END}")
                print(f"\nInstala manualmente:")
                print(f"  pip install {' '.join(python_paquetes)}")
    
    # Instalar FFmpeg si falta
    if ffmpeg_falta:
        print(f"\n{Colors.YELLOW}FFmpeg no esta instalado{Colors.END}")
        instalar = input("Instalar FFmpeg? (s/n): ")
        if instalar.lower() == 's':
            install_system_ffmpeg()
    
    return True

def install_system_ffmpeg():
    """Instala FFmpeg en el sistema"""
    sistema = get_system()
    distro = get_linux_distro()
    
    if sistema == 'linux':
        print(f"\nInstalando FFmpeg en Linux ({distro})...")
        
        if distro in ['ubuntu', 'debian', 'mint']:
            try:
                subprocess.run(['sudo', 'apt', 'update'], check=False)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True)
                print(f"{Colors.GREEN}FFmpeg instalado correctamente{Colors.END}")
                return True
            except:
                print(f"{Colors.RED}Error instalando FFmpeg{Colors.END}")
                return False
        
        elif distro in ['fedora']:
            try:
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'ffmpeg'], check=True)
                print(f"{Colors.GREEN}FFmpeg instalado correctamente{Colors.END}")
                return True
            except:
                print(f"{Colors.RED}Error instalando FFmpeg{Colors.END}")
                return False
        
        elif distro in ['arch', 'manjaro']:
            try:
                subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'], check=True)
                print(f"{Colors.GREEN}FFmpeg instalado correctamente{Colors.END}")
                return True
            except:
                print(f"{Colors.RED}Error instalando FFmpeg{Colors.END}")
                return False
    
    elif sistema == 'darwin':
        if check_command('brew'):
            try:
                subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
                print(f"{Colors.GREEN}FFmpeg instalado correctamente{Colors.END}")
                return True
            except:
                print(f"{Colors.RED}Error instalando FFmpeg{Colors.END}")
                return False
        else:
            print(f"{Colors.YELLOW}Instala Homebrew primero: https://brew.sh/{Colors.END}")
            return False
    
    elif sistema == 'windows':
        print(f"{Colors.YELLOW}Descarga FFmpeg desde: https://ffmpeg.org/download.html{Colors.END}")
        print("Instrucciones:")
        print("  1. Descarga el archivo")
        print("  2. Extrae en C:\\ffmpeg")
        print("  3. Agrega C:\\ffmpeg\\bin al PATH")
        return False
    
    return False

def mostrar_ayuda():
    """Muestra ayuda de uso"""
    ayuda = f"""
{Colors.BOLD}USO DE XONIMET:{Colors.END}

  python start.py [archivo] [opciones]

{Colors.BOLD}EJEMPLOS:{Colors.END}

  Analizar una imagen:
    python start.py foto.jpg

  Analizar un audio:
    python start.py cancion.mp3

  Analizar un video:
    python start.py video.mp4

  Analizar un documento:
    python start.py documento.pdf

  Salida en formato JSON:
    python start.py archivo.jpg --json

{Colors.BOLD}ARCHIVOS SOPORTADOS:{Colors.END}

  - Imagenes: .jpg, .png, .gif, .bmp, .tiff
  - Audio: .mp3, .flac, .wav, .ogg, .m4a
  - Video: .mp4, .avi, .mov, .mkv, .wmv
  - Documentos: .pdf, .docx, .xlsx, .pptx
  - Texto: .txt, .csv, .json, .html, .py
    """
    print(ayuda)

def verificar_importaciones():
    """Verifica que todas las importaciones necesarias funcionen"""
    print(f"\n{Colors.BOLD}Verificando importaciones...{Colors.END}")
    
    modulos = [
        ('PIL', 'Pillow'),
        ('mutagen', 'mutagen'),
        ('ffmpeg', 'ffmpeg-python'),
        ('PyPDF2', 'PyPDF2'),
        ('docx', 'python-docx'),
        ('openpyxl', 'openpyxl'),
        ('pptx', 'python-pptx'),
        ('exifread', 'exifread')
    ]
    
    todos_ok = True
    for modulo, nombre in modulos:
        try:
            __import__(modulo)
            print(f"{Colors.GREEN}  - {nombre}: OK{Colors.END}")
        except ImportError:
            print(f"{Colors.RED}  - {nombre}: FALLO{Colors.END}")
            todos_ok = False
    
    return todos_ok

def main():
    """Funcion principal"""
    # Limpiar pantalla
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    # Mostrar banner
    print_banner()
    
    # Verificar si hay argumentos de ayuda
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '/?']:
        mostrar_ayuda()
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no esta instalado{Colors.END}")
        print("Instala Python desde: https://www.python.org/downloads/")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    python_version = subprocess.run(get_python_command() + ['--version'], 
                                   capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {python_version}")
    print(f"{Colors.BOLD}Directorio:{Colors.END} {os.path.dirname(os.path.abspath(__file__))}")
    
    # Verificar dependencias
    faltantes = check_dependencies()
    
    if faltantes:
        print(f"\n{Colors.YELLOW}Faltan dependencias{Colors.END}")
        respuesta = input("Instalar automaticamente? (s/n): ")
        
        if respuesta.lower() == 's':
            install_dependencies(faltantes)
        else:
            print(f"\nPuedes instalarlas manualmente con:")
            print("  pip install pillow mutagen ffmpeg-python pypdf2 python-docx openpyxl python-pptx exifread")
            if 'ffmpeg-sistema' in faltantes:
                print("\nY FFmpeg segun tu sistema:")
                if get_system() == 'linux':
                    print("  sudo apt install ffmpeg  # Ubuntu/Debian")
                    print("  sudo pacman -S ffmpeg    # Arch")
                    print("  sudo dnf install ffmpeg  # Fedora")
    
    # Verificar que existe xonimet.py
    if not os.path.exists('xonimet.py'):
        print(f"\n{Colors.RED}Error: No se encuentra xonimet.py{Colors.END}")
        print("Asegurate de que xonimet.py esta en el mismo directorio")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar que las importaciones funcionan
    print(f"\n{Colors.BOLD}Verificando que todo funcione...{Colors.END}")
    if not verificar_importaciones():
        print(f"\n{Colors.YELLOW}Algunas importaciones fallaron{Colors.END}")
        print("El programa puede funcionar con funcionalidad limitada")
    
    # Verificar si se paso un archivo como argumento
    archivo_args = []
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        if os.path.exists(archivo):
            print(f"\n{Colors.BOLD}Archivo a analizar:{Colors.END} {archivo}")
            archivo_args = sys.argv[1:]
        else:
            print(f"\n{Colors.YELLOW}Advertencia: El archivo '{archivo}' no existe{Colors.END}")
            print("Se iniciara el modo interactivo")
    
    print(f"\n{Colors.BOLD}Iniciando XONIMET...{Colors.END}")
    print(f"{Colors.BOLD}Para salir:{Colors.END} Ctrl+C")
    print("-" * 60)
    
    # EJECUTAR XONIMET.PY - ESTA ES LA PARTE IMPORTANTE
    try:
        python_cmd = get_python_command()
        cmd = python_cmd + ['xonimet.py'] + archivo_args
        print(f"Ejecutando: {' '.join(cmd)}")
        print("-" * 60)
        
        # Ejecutar xonimet.py
        resultado = subprocess.run(cmd)
        
        if resultado.returncode != 0:
            print(f"\n{Colors.RED}Error: xonimet.py termino con codigo {resultado.returncode}{Colors.END}")
            
    except FileNotFoundError:
        print(f"\n{Colors.RED}Error: No se encuentra xonimet.py{Colors.END}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Programa detenido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error ejecutando xonimet.py: {e}{Colors.END}")
    
    print(f"\n{Colors.BLUE}Gracias por usar XONIMET 2026{Colors.END}")
    print(f"{Colors.BLUE}Desarrollado por Darian Alberto Camacho Salas{Colors.END}")
    
    if get_system() != 'windows':
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

def crear_accesos_directos():
    """Crea accesos directos para cada sistema"""
    sistema = get_system()
    
    if sistema == 'windows':
        # Crear .bat para Windows
        with open('INICIAR_XONIMET.bat', 'w') as f:
            f.write("""@echo off
title XONIMET 2026 - Extractor de Metadatos
color 1F
echo ========================================
echo      XONIMET 2026 - Extractor Universal
echo      Desarrollado por Darian Alberto
echo ========================================
echo.
echo Arrastra un archivo a esta ventana para analizarlo
echo O escribe la ruta del archivo:
echo.
set /p "archivo=Archivo: "
python start.py %archivo%
pause
""")
        print(f"{Colors.GREEN}Creado INICIAR_XONIMET.bat - Haz doble clic para ejecutar{Colors.END}")
    
    elif sistema == 'linux':
        # Crear .sh para Linux
        with open('INICIAR_XONIMET.sh', 'w') as f:
            f.write("""#!/bin/bash
echo "========================================"
echo "      XONIMET 2026 - Extractor Universal"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
echo "Arrastra un archivo a la terminal o escribe su ruta:"
read -p "Archivo: " archivo
python3 start.py $archivo
read -p "Presiona Enter para salir"
""")
        os.chmod('INICIAR_XONIMET.sh', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONIMET.sh - Ejecuta con: ./INICIAR_XONIMET.sh{Colors.END}")
    
    elif sistema == 'darwin':
        # Crear .command para Mac
        with open('INICIAR_XONIMET.command', 'w') as f:
            f.write("""#!/bin/bash
cd "$(dirname "$0")"
echo "========================================"
echo "      XONIMET 2026 - Extractor Universal"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
python3 start.py
""")
        os.chmod('INICIAR_XONIMET.command', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONIMET.command - Haz doble clic para ejecutar{Colors.END}")

if __name__ == '__main__':
    try:
        # Crear accesos directos
        crear_accesos_directos()
        
        # Ejecutar programa principal
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
