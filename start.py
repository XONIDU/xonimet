#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONIMET 2026 - Extractor Universal de Metadatos - Installer
Este script ejecuta xonimet.py y verifica/instala dependencias
con múltiples estrategias de fallback para todas las plataformas.
Desarrollado por: Darian Alberto Camacho Salas
#Somos XONIDU
"""

import subprocess
import sys
import os
import platform
import shutil
import importlib.util
import time

# ============================================================================
# Colores para terminal
# ============================================================================
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

# ============================================================================
# Detección del sistema
# ============================================================================
def get_system():
    return platform.system().lower()

def get_linux_distro():
    if get_system() != 'linux':
        return None
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content or 'mint' in content:
                    return 'debian-based'
                elif 'arch' in content or 'manjaro' in content:
                    return 'arch-based'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'opensuse' in content:
                    return 'opensuse'
                elif 'centos' in content or 'rhel' in content:
                    return 'rhel-based'
        if shutil.which('apt'):
            return 'debian-based'
        elif shutil.which('pacman'):
            return 'arch-based'
        elif shutil.which('dnf'):
            return 'fedora'
        elif shutil.which('zypper'):
            return 'opensuse'
        elif shutil.which('yum'):
            return 'rhel-based'
        return 'linux-generic'
    except:
        return 'linux-generic'

def get_python_command():
    if get_system() == 'windows':
        return ['python']
    else:
        for cmd in ['python3', 'python']:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True)
                return [cmd]
            except:
                continue
        return ['python3']

def get_pip_commands():
    """Retorna múltiples comandos pip posibles en orden de preferencia"""
    cmds = []
    python_cmd = get_python_command()[0]
    
    # Opción 1: python -m pip
    cmds.append([sys.executable, '-m', 'pip'])
    
    # Opción 2: pip3
    if shutil.which('pip3'):
        cmds.append(['pip3'])
    
    # Opción 3: pip
    if shutil.which('pip'):
        cmds.append(['pip'])
    
    # Opción 4: python3 -m pip
    if python_cmd != sys.executable:
        cmds.append([python_cmd, '-m', 'pip'])
    
    return cmds

def get_install_strategies(packages):
    """Genera múltiples estrategias de instalación para fallback"""
    strategies = []
    system = get_system()
    distro = get_linux_distro()
    
    # Estrategia 1: pip con --break-system-packages (Arch/Fedora modernos)
    strategies.append(['--break-system-packages'])
    
    # Estrategia 2: pip con --user (evita permisos)
    strategies.append(['--user'])
    
    # Estrategia 3: pip normal
    strategies.append([])
    
    # Estrategia 4: pip con --ignore-installed (forzar)
    strategies.append(['--ignore-installed'])
    
    # Estrategia 5: pip con --no-deps (solo el paquete)
    strategies.append(['--no-deps'])
    
    # Estrategias específicas por sistema
    if system == 'linux':
        if distro in ['debian-based']:
            strategies.insert(1, ['--system'])  # Debian/Ubuntu
        elif distro in ['arch-based', 'fedora']:
            strategies.insert(0, ['--break-system-packages'])
    elif system == 'darwin':
        strategies.append(['--user'])
    elif system == 'windows':
        strategies.append(['--no-warn-script-location'])
    
    return strategies

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_xonimet_path():
    """Detecta la ruta de xonimet.py en múltiples ubicaciones"""
    script_dir = get_script_dir()
    rutas = [
        os.path.join(script_dir, 'xonimet.py'),
        '/usr/share/xonimet/xonimet.py',
        os.path.join(os.path.expanduser("~"), '.xonimet', 'xonimet.py'),
        os.path.join(os.getcwd(), 'xonimet.py')
    ]
    for r in rutas:
        if os.path.exists(r):
            return r
    return None

def print_banner():
    sistema = get_system()
    distro = get_linux_distro()
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'UNKNOWN')
    
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}═══════════════════════════════════════════════════════════
                    XONIMET 2026 v2.1                    
              Extractor Universal de Metadatos            
              Extrae informacion de: Fotos, Audio,        
              Video, Documentos y mas                     
                                                          
              Sistema detectado: {sistema_texto}            
                                                          
              Desarrollado por: Darian Alberto            
              Camacho Salas                               
              #Somos XONIDU
═══════════════════════════════════════════════════════════{Colors.END}
    """
    print(banner)

def mostrar_ayuda():
    ayuda = f"""
{Colors.BOLD}USO DE XONIMET:{Colors.END}

  python start.py [archivo] [opciones]

{Colors.BOLD}DESCRIPCION:{Colors.END}

  XONIMET es un extractor universal de metadatos que analiza
  archivos, fotos, audio, video y documentos.

{Colors.BOLD}EJEMPLOS:{Colors.END}

  Modo interactivo:
    python start.py

  Analizar un archivo:
    python start.py foto.jpg
    python start.py cancion.mp3
    python start.py video.mp4

  Guardar resultados en JSON:
    python start.py documento.pdf --json

  Generar reporte PDF:
    python start.py video.mp4 --pdf

{Colors.BOLD}ARCHIVOS SOPORTADOS:{Colors.END}

  Fotos: .jpg, .png, .gif, .bmp, .tiff
  Audio: .mp3, .flac, .wav, .ogg, .m4a
  Video: .mp4, .avi, .mov, .mkv, .wmv
  Documentos: .pdf, .docx, .xlsx, .pptx
  Texto: .txt, .csv, .json, .py, .html
    """
    print(ayuda)

# ============================================================================
# Verificación de dependencias
# ============================================================================
def check_python():
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_pip():
    """Verifica si pip está disponible con múltiples comandos"""
    for pip_cmd in get_pip_commands():
        try:
            subprocess.run(pip_cmd + ['--version'], capture_output=True, check=True)
            return True, pip_cmd
        except:
            continue
    return False, None

def install_pip_linux():
    """Instala pip en múltiples distribuciones Linux"""
    distro = get_linux_distro()
    print(f"{Colors.YELLOW}Instalando pip en Linux ({distro})...{Colors.END}")
    
    instaladores = []
    if distro == 'debian-based':
        instaladores = [
            ['sudo', 'apt', 'update'],
            ['sudo', 'apt', 'install', '-y', 'python3-pip']
        ]
    elif distro == 'arch-based':
        instaladores = [
            ['sudo', 'pacman', '-S', '--noconfirm', 'python-pip']
        ]
    elif distro == 'fedora':
        instaladores = [
            ['sudo', 'dnf', 'install', '-y', 'python3-pip']
        ]
    elif distro == 'opensuse':
        instaladores = [
            ['sudo', 'zypper', 'refresh'],
            ['sudo', 'zypper', 'install', '-y', 'python3-pip']
        ]
    elif distro == 'rhel-based':
        instaladores = [
            ['sudo', 'yum', 'install', '-y', 'python3-pip']
        ]
    else:
        # Fallback: ensurepip
        instaladores = [
            [sys.executable, '-m', 'ensurepip', '--upgrade']
        ]
    
    for cmd in instaladores:
        try:
            subprocess.run(cmd, check=True)
            return True
        except:
            continue
    return False

def install_pip_windows():
    """Instala pip en Windows"""
    print(f"{Colors.YELLOW}Instalando pip en Windows...{Colors.END}")
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        return True
    except:
        try:
            import urllib.request
            urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')
            subprocess.run([sys.executable, 'get-pip.py'], check=True)
            os.remove('get-pip.py')
            return True
        except:
            return False

def check_python_module(module_name):
    return importlib.util.find_spec(module_name) is not None

def check_dependencies():
    """Verifica las dependencias necesarias"""
    print(f"\n{Colors.BOLD}Verificando dependencias...{Colors.END}")
    
    dependencies = [
        ('PIL', 'pillow', 'Imagenes'),
        ('mutagen', 'mutagen', 'Audio'),
        ('ffmpeg', 'ffmpeg-python', 'Video'),
        ('PyPDF2', 'pypdf2', 'PDF'),
        ('docx', 'python-docx', 'Word'),
        ('openpyxl', 'openpyxl', 'Excel'),
        ('pptx', 'python-pptx', 'PowerPoint'),
        ('exifread', 'exifread', 'EXIF'),
        ('reportlab', 'reportlab', 'Reportes PDF'),
    ]
    
    missing = []
    for module, package, desc in dependencies:
        import_name = module if module != 'PIL' else 'PIL'
        if module == 'ffmpeg':
            import_name = 'ffmpeg'
        
        try:
            __import__(import_name)
            print(f"{Colors.GREEN}  - {package} ({desc}): OK{Colors.END}")
        except ImportError:
            print(f"{Colors.YELLOW}  - {package} ({desc}): FALTANTE{Colors.END}")
            missing.append(package)
    
    return missing

def install_with_pip(packages):
    """Intenta instalar paquetes con múltiples estrategias"""
    if not packages:
        return True
    
    pip_ok, pip_cmd = check_pip()
    if not pip_ok:
        print(f"{Colors.RED}No se encontró pip. Intentando instalar...{Colors.END}")
        sistema = get_system()
        if sistema == 'linux':
            if not install_pip_linux():
                print(f"{Colors.RED}No se pudo instalar pip automáticamente{Colors.END}")
                return False
        elif sistema == 'windows':
            if not install_pip_windows():
                print(f"{Colors.RED}No se pudo instalar pip automáticamente{Colors.END}")
                return False
        pip_ok, pip_cmd = check_pip()
        if not pip_ok:
            return False
    
    strategies = get_install_strategies(packages)
    pip_base = pip_cmd if pip_cmd else ['pip']
    
    for flags in strategies:
        cmd = pip_base + ['install'] + flags + packages
        flag_desc = ' '.join(flags) if flags else '(sin flags)'
        print(f"\n  Intentando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print(f"{Colors.GREEN}  ✓ Éxito con {flag_desc}{Colors.END}")
                return True
            else:
                error_msg = result.stderr[:200] if result.stderr else result.stdout[:200]
                print(f"{Colors.YELLOW}  ✗ Falló: {error_msg}{Colors.END}")
        except subprocess.TimeoutExpired:
            print(f"{Colors.YELLOW}  ✗ Timeout{Colors.END}")
        except Exception as e:
            print(f"{Colors.YELLOW}  ✗ Error: {str(e)[:100]}{Colors.END}")
    
    # Último intento: pipx si está disponible
    if shutil.which('pipx'):
        print(f"\n  Intentando con pipx...")
        for pkg in packages:
            try:
                subprocess.run(['pipx', 'install', pkg], capture_output=True, timeout=60)
                print(f"{Colors.GREEN}  ✓ {pkg} instalado con pipx{Colors.END}")
            except:
                continue
        return True
    
    print(f"{Colors.RED}No se pudieron instalar las dependencias automáticamente{Colors.END}")
    return False

def check_ffmpeg_system():
    """Verifica si FFmpeg está instalado en el sistema"""
    print(f"\n{Colors.BOLD}Verificando FFmpeg...{Colors.END}")
    
    if shutil.which('ffmpeg'):
        print(f"{Colors.GREEN}  - FFmpeg: OK{Colors.END}")
        return True
    else:
        print(f"{Colors.YELLOW}  - FFmpeg: NO INSTALADO (necesario para videos){Colors.END}")
        return False

def install_ffmpeg_system():
    """Instala FFmpeg según el sistema"""
    sistema = get_system()
    distro = get_linux_distro()
    
    print(f"{Colors.YELLOW}Instalando FFmpeg...{Colors.END}")
    
    instaladores = []
    if sistema == 'linux':
        if distro == 'debian-based':
            instaladores = [['sudo', 'apt', 'update'], ['sudo', 'apt', 'install', '-y', 'ffmpeg']]
        elif distro == 'arch-based':
            instaladores = [['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg']]
        elif distro == 'fedora':
            instaladores = [['sudo', 'dnf', 'install', '-y', 'ffmpeg']]
        elif distro == 'opensuse':
            instaladores = [['sudo', 'zypper', 'refresh'], ['sudo', 'zypper', 'install', '-y', 'ffmpeg']]
        else:
            instaladores = [['sudo', 'apt', 'install', '-y', 'ffmpeg']]
    elif sistema == 'darwin':
        if shutil.which('brew'):
            instaladores = [['brew', 'install', 'ffmpeg']]
        else:
            print(f"{Colors.YELLOW}Instala Homebrew primero: https://brew.sh/{Colors.END}")
            return False
    elif sistema == 'windows':
        print(f"{Colors.YELLOW}Descarga FFmpeg manualmente desde: https://ffmpeg.org/download.html{Colors.END}")
        return False
    
    for cmd in instaladores:
        try:
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}FFmpeg instalado correctamente{Colors.END}")
            return True
        except:
            continue
    
    return False

def verify_imports():
    """Verifica que todas las importaciones funcionen"""
    print(f"\n{Colors.BOLD}Verificando importaciones...{Colors.END}")
    
    modules = [
        ('PIL', 'Pillow'),
        ('mutagen', 'mutagen'),
        ('ffmpeg', 'ffmpeg-python'),
        ('PyPDF2', 'PyPDF2'),
        ('docx', 'python-docx'),
        ('openpyxl', 'openpyxl'),
        ('pptx', 'python-pptx'),
        ('exifread', 'exifread'),
        ('reportlab', 'reportlab'),
    ]
    
    all_ok = True
    for module, name in modules:
        import_name = module if module != 'PIL' else 'PIL'
        if module == 'ffmpeg':
            import_name = 'ffmpeg'
        try:
            __import__(import_name)
            print(f"{Colors.GREEN}  - {name}: OK{Colors.END}")
        except ImportError:
            print(f"{Colors.RED}  - {name}: FALLÓ{Colors.END}")
            all_ok = False
    
    return all_ok

def create_shortcuts():
    """Crea accesos directos para cada sistema"""
    system = get_system()
    
    if system == 'windows':
        with open('XONIMET.bat', 'w') as f:
            f.write("""@echo off
title XONIMET 2026 - Extractor de Metadatos
color 1F
echo ========================================
echo      XONIMET 2026 - Extractor Universal
echo      Desarrollado por Darian Alberto Camacho Salas
echo      #Somos XONIDU
echo ========================================
echo.
python start.py %*
pause
""")
        print(f"{Colors.GREEN}Creado XONIMET.bat{Colors.END}")
    elif system == 'linux':
        with open('XONIMET.sh', 'w') as f:
            f.write("""#!/bin/bash
echo "========================================"
echo "      XONIMET 2026 - Extractor Universal"
echo "      Desarrollado por Darian Alberto Camacho Salas"
echo "      #Somos XONIDU"
echo "========================================"
echo ""
python3 start.py "$@"
read -p "Presiona Enter para salir"
""")
        os.chmod('XONIMET.sh', 0o755)
        print(f"{Colors.GREEN}Creado XONIMET.sh{Colors.END}")
    elif system == 'darwin':
        with open('XONIMET.command', 'w') as f:
            f.write("""#!/bin/bash
cd "$(dirname "$0")"
echo "========================================"
echo "      XONIMET 2026 - Extractor Universal"
echo "      Desarrollado por Darian Alberto Camacho Salas"
echo "      #Somos XONIDU"
echo "========================================"
echo ""
python3 start.py "$@"
""")
        os.chmod('XONIMET.command', 0o755)
        print(f"{Colors.GREEN}Creado XONIMET.command{Colors.END}")

# ============================================================================
# Función principal
# ============================================================================
def main():
    # Limpiar pantalla
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    print_banner()
    
    # Mostrar ayuda
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '/?']:
        mostrar_ayuda()
        if get_system() != 'windows':
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no esta instalado{Colors.END}")
        print("Descarga desde: https://www.python.org/downloads/")
        sys.exit(1)
    
    python_version = subprocess.run(get_python_command() + ['--version'], capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {python_version}")
    print(f"{Colors.BOLD}Directorio:{Colors.END} {get_script_dir()}")
    
    # Verificar/instalar pip
    pip_ok, _ = check_pip()
    if not pip_ok:
        print(f"\n{Colors.YELLOW}Pip no encontrado. Instalando...{Colors.END}")
        sistema = get_system()
        if sistema == 'linux':
            if not install_pip_linux():
                print(f"{Colors.RED}No se pudo instalar pip automáticamente{Colors.END}")
                sys.exit(1)
        elif sistema == 'windows':
            if not install_pip_windows():
                print(f"{Colors.RED}No se pudo instalar pip automáticamente{Colors.END}")
                sys.exit(1)
    
    # Verificar dependencias
    missing = check_dependencies()
    if missing:
        print(f"\n{Colors.YELLOW}Faltan {len(missing)} dependencias: {', '.join(missing)}{Colors.END}")
        respuesta = input("Instalar automaticamente? (s/n): ")
        if respuesta.lower() == 's':
            if not install_with_pip(missing):
                print(f"{Colors.YELLOW}Instalacion automatica fallida. Puedes instalar manualmente:{Colors.END}")
                print(f"  pip install {' '.join(missing)}")
                if get_system() == 'linux':
                    print("  O con: pip install --break-system-packages " + ' '.join(missing))
    
    # Verificar FFmpeg
    if not check_ffmpeg_system():
        respuesta = input("\nInstalar FFmpeg? (s/n): ")
        if respuesta.lower() == 's':
            install_ffmpeg_system()
    
    # Verificar importaciones
    verify_imports()
    
    # Crear accesos directos
    create_shortcuts()
    
    # Crear directorio de configuracion
    config_dir = os.path.join(os.path.expanduser("~"), '.xonimet')
    os.makedirs(config_dir, exist_ok=True)
    print(f"{Colors.GREEN}Configuracion en: {config_dir}{Colors.END}")
    
    # Buscar xonimet.py
    xonimet_path = get_xonimet_path()
    if not xonimet_path:
        print(f"\n{Colors.RED}Error: No se encuentra xonimet.py{Colors.END}")
        sys.exit(1)
    
    print(f"\n{Colors.BOLD}Iniciando XONIMET...{Colors.END}")
    print(f"{Colors.CYAN}Para salir: Ctrl+C{Colors.END}")
    print("-" * 50)
    
    try:
        python_cmd = get_python_command()
        cmd = python_cmd + [xonimet_path] + sys.argv[1:]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Programa detenido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}")
    
    print(f"\n{Colors.GREEN}Gracias por usar XONIMET 2026{Colors.END}")
    print(f"{Colors.GREEN}Desarrollado por Darian Alberto Camacho Salas{Colors.END}")
    print(f"{Colors.GREEN}#Somos XONIDU{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
