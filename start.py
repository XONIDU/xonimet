#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONIMET 2026 - Lanzador Universal
Este script detecta el sistema, instala dependencias y ejecuta xonimet.py
Genera un archivo .bat en Windows para ejecutar con permisos de administrador
Desarrollado por: Darian Alberto Camacho Salas
"""

import subprocess
import sys
import os
import webbrowser
import time
import platform
import threading
import ctypes

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

# Dependencias necesarias para xonimet.py
REQUISITOS = [
    'pillow>=10.0.0',
    'mutagen>=1.46.0',
    'ffmpeg-python>=0.2.0',
    'PyPDF2>=3.0.0',
    'python-docx>=0.8.11',
    'openpyxl>=3.1.0',
    'python-pptx>=0.6.21',
    'exifread>=3.0.0',
    'reportlab>=4.0.0'
]

def is_admin():
    """Verifica si el script se ejecuta como administrador en Windows"""
    if platform.system() == 'Windows':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    return True

def get_system():
    """Detecta el sistema operativo"""
    return platform.system().lower()

def get_linux_distro():
    """Detecta la distribución de Linux específica"""
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
                elif 'opensuse' in content:
                    return 'opensuse'
        
        try:
            result = subprocess.run(['lsb_release', '-i'], capture_output=True, text=True)
            if 'Ubuntu' in result.stdout:
                return 'ubuntu'
            elif 'Debian' in result.stdout:
                return 'debian'
            elif 'Fedora' in result.stdout:
                return 'fedora'
            elif 'CentOS' in result.stdout:
                return 'centos'
        except:
            pass
        
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    """Obtiene el comando Python correcto según el sistema"""
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def get_pip_command():
    """Obtiene el comando pip correcto según el sistema"""
    if get_system() == 'windows':
        return [sys.executable, '-m', 'pip']
    else:
        return [sys.executable, '-m', 'pip']

def get_install_flags():
    """Obtiene los flags de instalación según el sistema"""
    flags = []
    sistema = get_system()
    distro = get_linux_distro()
    
    if sistema == 'linux':
        if distro in ['ubuntu', 'debian', 'mint', 'arch', 'manjaro', 'fedora']:
            flags.append('--break-system-packages')
        else:
            flags.append('--user')
    elif sistema == 'darwin':
        flags.append('--user')
    
    return flags

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
{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                     XONIMET 2026 v2.0                     ║
║              Extractor Universal de Metadatos              ║
║                                                            ║
║               Sistema detectado: {sistema_texto}            ║
║                                                            ║
║               Desarrollado por: Darian Alberto               ║
║                      Camacho Salas                           ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

def check_python():
    """Verifica que Python está instalado"""
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_pip():
    """Verifica que pip está instalado y funciona"""
    try:
        cmd = get_pip_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def install_pip_windows():
    """Instala pip en Windows si no está disponible"""
    print(f"{Colors.YELLOW}Pip no encontrado. Instalando pip...{Colors.END}")
    try:
        import urllib.request
        print("  Descargando get-pip.py...")
        urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')
        
        print("  Instalando pip...")
        subprocess.run([sys.executable, 'get-pip.py'], check=True)
        
        os.remove('get-pip.py')
        
        print(f"{Colors.GREEN}  Pip instalado correctamente{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}  Error instalando pip: {e}{Colors.END}")
        return False

def check_ffmpeg():
    """Verifica si FFmpeg está instalado en el sistema"""
    print(f"\n{Colors.BOLD}Verificando FFmpeg...{Colors.END}")
    
    if check_command('ffmpeg'):
        print(f"{Colors.GREEN}  - FFmpeg OK{Colors.END}")
        return True
    else:
        print(f"{Colors.YELLOW}  - FFmpeg (faltante - necesario para videos){Colors.END}")
        return False

def check_command(comando):
    """Verifica si un comando existe en el sistema"""
    return subprocess.run(['which', comando], capture_output=True).returncode == 0 if get_system() != 'windows' else subprocess.run(['where', comando], capture_output=True).returncode == 0

def check_dependencies():
    """Verifica qué dependencias necesita xonimet.py"""
    print(f"\n{Colors.BOLD}Verificando dependencias de Python...{Colors.END}")
    
    missing = []
    for req in REQUISITOS:
        package = req.split('>=')[0].split('==')[0]
        import_name = package.replace('-', '_')
        if import_name == 'pillow':
            import_name = 'PIL'
        elif import_name == 'ffmpeg_python':
            import_name = 'ffmpeg'
        
        try:
            __import__(import_name)
            print(f"{Colors.GREEN}  - {package} OK{Colors.END}")
        except ImportError:
            print(f"{Colors.YELLOW}  - {package} (faltante){Colors.END}")
            missing.append(req)
    
    return missing

def install_dependencies(missing):
    """Instala las dependencias faltantes según el sistema"""
    if not missing:
        print(f"\n{Colors.GREEN}Todas las dependencias estan instaladas{Colors.END}")
        return True
    
    print(f"\n{Colors.BOLD}Instalando dependencias faltantes...{Colors.END}")
    
    pip_cmd = get_pip_command()
    flags = get_install_flags()
    
    sistema = get_system()
    distro = get_linux_distro()
    
    print(f"{Colors.YELLOW}Sistema: {sistema}{Colors.END}")
    if distro:
        print(f"{Colors.YELLOW}Distribucion: {distro}{Colors.END}")
    if flags:
        print(f"{Colors.YELLOW}Flags: {' '.join(flags)}{Colors.END}")
    
    success = True
    for req in missing:
        print(f"  Instalando {req}...")
        try:
            cmd = pip_cmd + ['install', req] + flags
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}  - {req} instalado{Colors.END}")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}  Error instalando {req}{Colors.END}")
            success = False
    
    if success:
        print(f"\n{Colors.GREEN}Todas las dependencias instaladas correctamente{Colors.END}")
    else:
        print(f"\n{Colors.YELLOW}Algunas dependencias no se instalaron{Colors.END}")
        print(f"   Puedes instalarlas manualmente con:")
        print(f"   {get_install_command()}")
    
    return success

def install_ffmpeg():
    """Instala FFmpeg según el sistema"""
    sistema = get_system()
    distro = get_linux_distro()
    
    print(f"\n{Colors.BOLD}Instalando FFmpeg...{Colors.END}")
    
    if sistema == 'windows':
        print(f"{Colors.YELLOW}En Windows, descarga FFmpeg manualmente:{Colors.END}")
        print("  1. Ve a: https://ffmpeg.org/download.html")
        print("  2. Descarga la version para Windows")
        print("  3. Extrae en C:\\ffmpeg")
        print("  4. Agrega C:\\ffmpeg\\bin al PATH")
        return False
    
    elif sistema == 'linux':
        if distro in ['ubuntu', 'debian', 'mint']:
            try:
                subprocess.run(['sudo', 'apt', 'update'], check=False)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True)
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
        
        elif distro in ['fedora']:
            try:
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'ffmpeg'], check=True)
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
    
    return False

def get_install_command():
    """Obtiene el comando de instalación según el sistema"""
    sistema = get_system()
    distro = get_linux_distro()
    
    if sistema == 'windows':
        return "pip install -r requirements.txt"
    elif sistema == 'linux':
        if distro in ['ubuntu', 'debian', 'mint', 'arch', 'manjaro', 'fedora']:
            return "pip install -r requirements.txt --break-system-packages"
        else:
            return "pip install --user -r requirements.txt"
    elif sistema == 'darwin':
        return "pip3 install -r requirements.txt --user"
    else:
        return "pip install -r requirements.txt"

def create_windows_bat():
    """Crea un archivo .bat para ejecutar con permisos de administrador"""
    sistema = get_system()
    if sistema != 'windows':
        return
    
    bat_content = '''@echo off
title XONIMET 2026 - Extractor de Metadatos
color 1F
cls

echo ========================================
echo      XONIMET 2026 - Extractor Universal
echo      Desarrollado por Darian Alberto
echo ========================================
echo.

:: Verificar si se ejecuta como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Se requieren permisos de administrador para instalar dependencias
    echo.
    echo Solicitando permisos...
    echo.
    
    :: Crear script temporal para ejecutar con admin
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\\getadmin.vbs"
    "%temp%\\getadmin.vbs"
    del "%temp%\\getadmin.vbs"
    exit /B
)

echo [OK] Permisos de administrador obtenidos
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo IMPORTANTE: Marca "Add Python to PATH" durante la instalacion
    pause
    start https://www.python.org/downloads/
    exit
)

echo [OK] Python instalado
python --version
echo.

:: Verificar pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Pip no encontrado. Instalando pip...
    python -m ensurepip --upgrade
)

echo [OK] Pip disponible
echo.

:: Instalar dependencias
echo Instalando dependencias necesarias...
python -m pip install pillow>=10.0.0
python -m pip install mutagen>=1.46.0
python -m pip install ffmpeg-python>=0.2.0
python -m pip install PyPDF2>=3.0.0
python -m pip install python-docx>=0.8.11
python -m pip install openpyxl>=3.1.0
python -m pip install python-pptx>=0.6.21
python -m pip install exifread>=3.0.0
python -m pip install reportlab>=4.0.0
echo.
echo [OK] Dependencias instaladas
echo.

:: Iniciar XONIMET
echo ========================================
echo Iniciando XONIMET...
echo ========================================
echo.
python xonimet.py

pause
'''
    
    bat_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'XONIMET_ADMIN.bat')
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    print(f"{Colors.GREEN}Archivo XONIMET_ADMIN.bat creado - Ejecuta como administrador si hay problemas{Colors.END}")
    
    # Tambien crear un .bat simple sin admin
    simple_bat = '''@echo off
title XONIMET 2026
color 1F
python start.py
pause
'''
    simple_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'XONIMET.bat')
    with open(simple_path, 'w', encoding='utf-8') as f:
        f.write(simple_bat)
    print(f"{Colors.GREEN}Archivo XONIMET.bat creado - Doble clic para ejecutar{Colors.END}")

def mostrar_instrucciones_python():
    """Muestra instrucciones para instalar Python según el sistema"""
    sistema = get_system()
    distro = get_linux_distro()
    
    if sistema == 'windows':
        print(f"   Descarga Python desde: https://www.python.org/downloads/")
        print(f"   IMPORTANTE: Al instalar, marca 'Add Python to PATH'")
        print(f"   Luego cierra y vuelve a abrir la terminal")
    elif sistema == 'linux':
        if distro in ['ubuntu', 'debian', 'mint']:
            print(f"   Instala con: sudo apt update && sudo apt install python3 python3-pip")
        elif distro in ['fedora', 'centos']:
            print(f"   Instala con: sudo dnf install python3 python3-pip")
        elif distro in ['arch', 'manjaro']:
            print(f"   Instala con: sudo pacman -S python python-pip")
        else:
            print(f"   Instala Python 3 desde: https://www.python.org/downloads/")
    elif sistema == 'darwin':
        print(f"   Instala con: brew install python3")
        print(f"   O descarga desde: https://www.python.org/downloads/")

def main():
    """Funcion principal - Ejecuta xonimet.py"""
    # Limpiar pantalla según sistema
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    # Mostrar banner
    print_banner()
    
    sistema = get_system()
    distro = get_linux_distro()
    
    print(f"{Colors.BOLD}Sistema operativo:{Colors.END} {sistema}")
    if distro:
        print(f"{Colors.BOLD}Distribucion:{Colors.END} {distro}")
    print(f"{Colors.BOLD}Python:{Colors.END} {sys.version.split()[0]}")
    print(f"{Colors.BOLD}Ruta:{Colors.END} {os.path.dirname(os.path.abspath(__file__))}")
    
    # Crear archivos .bat para Windows (siempre)
    if sistema == 'windows':
        create_windows_bat()
        print()
    
    # Verificar que Python está instalado
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no esta instalado o no esta en el PATH{Colors.END}")
        mostrar_instrucciones_python()
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar pip en Windows e instalarlo si es necesario
    if sistema == 'windows' and not check_pip():
        print(f"\n{Colors.YELLOW}Pip no encontrado. Intentando instalar...{Colors.END}")
        if not install_pip_windows():
            print(f"\n{Colors.RED}No se pudo instalar pip automaticamente{Colors.END}")
            print(f"   Ejecuta XONIMET_ADMIN.bat como administrador")
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
            return
    
    # Verificar dependencias de Python
    missing = check_dependencies()
    
    # Instalar dependencias si faltan
    if missing:
        print(f"\n{Colors.YELLOW}Faltan {len(missing)} dependencias{Colors.END}")
        
        # En Windows, sugerir usar el .bat con admin
        if sistema == 'windows':
            print(f"\n{Colors.YELLOW}Se recomienda ejecutar XONIMET_ADMIN.bat como administrador{Colors.END}")
            print(f"   para instalar las dependencias automaticamente")
            respuesta = input(f"Intentar instalar ahora? (s/n): ")
        else:
            respuesta = input(f"Instalar ahora? (s/n): ")
        
        if respuesta.lower() == 's':
            if not install_dependencies(missing):
                print(f"\n{Colors.YELLOW}Continuando a pesar de errores...{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}No se instalaran dependencias. Puede haber errores.{Colors.END}")
            if sistema == 'windows':
                print(f"   Ejecuta XONIMET_ADMIN.bat como administrador para instalarlas")
    
    # Verificar FFmpeg (necesario para videos)
    if not check_ffmpeg():
        print(f"\n{Colors.YELLOW}FFmpeg no esta instalado (necesario para analizar videos){Colors.END}")
        respuesta = input(f"Instalar FFmpeg ahora? (s/n): ")
        if respuesta.lower() == 's':
            install_ffmpeg()
    
    # Verificar que existe xonimet.py
    if not os.path.exists('xonimet.py'):
        print(f"\n{Colors.RED}Error: No se encuentra xonimet.py{Colors.END}")
        print(f"   Asegurate de que xonimet.py esta en la misma carpeta")
        print(f"   Archivos encontrados: {', '.join(os.listdir('.')[:5])}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    print(f"\n{Colors.BOLD}Iniciando XONIMET (programa principal)...{Colors.END}")
    print(f"{Colors.BOLD}Para analizar un archivo, escribe su ruta en el menu interactivo{Colors.END}")
    print(f"{Colors.BOLD}Para salir del programa:{Colors.END} Ctrl+C")
    print("-" * 60)
    
    # Ejecutar xonimet.py
    try:
        python_cmd = get_python_command()
        print(f"{Colors.BOLD}Ejecutando:{Colors.END} {' '.join(python_cmd + ['xonimet.py'])}")
        print("-" * 60)
        
        subprocess.run(python_cmd + ['xonimet.py'])
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Programa detenido por el usuario{Colors.END}")
    except FileNotFoundError as e:
        print(f"\n{Colors.RED}Error: No se encuentra Python o xonimet.py{Colors.END}")
        print(f"   {e}")
    except Exception as e:
        print(f"\n{Colors.RED}Error ejecutando xonimet.py: {e}{Colors.END}")
    
    print(f"\n{Colors.BLUE}Gracias por usar XONIMET 2026{Colors.END}")
    print(f"{Colors.CYAN}Desarrollado por Darian Alberto Camacho Salas{Colors.END}")
    
    if sistema != 'windows':
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
