#!/usr/bin/env python3
"""
empaquetar.py
=============
Empaqueta la app en un ejecutable portable que NO requiere Python instalado.

Uso:
    python empaquetar.py

Requiere (instalar una sola vez):
    pip install pyinstaller flet yt-dlp

En Windows también necesitas:
    - FFmpeg en PATH, o coloca ffmpeg.exe en esta carpeta antes de empaquetar.

El ejecutable generado queda en:
    dist/DescargadorVideos/          ← carpeta portable
    dist/DescargadorVideos.exe       ← Windows (si usas --onefile)
"""

import os
import sys
import shutil
import subprocess
import platform

NOMBRE_APP   = "DescargadorVideos"
SCRIPT_MAIN  = "main.py"
ICONO        = "icon.ico"        # Opcional: pon tu .ico aquí
SO           = platform.system() # "Windows", "Linux", "Darwin"

def buscar_ffmpeg():
    ruta = shutil.which("ffmpeg")
    if ruta:
        print(f"  ✅ FFmpeg encontrado: {ruta}")
    else:
        print("  ⚠️  FFmpeg NO detectado en PATH.")
        print("     El .exe funcionará para modo WhatsApp.")
        print("     Para HD y MP3: coloca ffmpeg.exe en la misma carpeta que el ejecutable.")
    return ruta

def main():
    print("\n╔══════════════════════════════════════╗")
    print("║  EMPAQUETADOR — Descargador Videos   ║")
    print("╚══════════════════════════════════════╝\n")

    print(f"  Sistema: {SO}")
    ffmpeg_path = buscar_ffmpeg()

    # ── Construir comando PyInstaller ──
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name", NOMBRE_APP,
        "--windowed",          # Sin consola negra en Windows
        "--onedir",            # Carpeta portable (más rápido que --onefile)
        # Datos de Flet (assets internos)
        "--collect-data", "flet",
        "--collect-data", "flet_core",
        # Módulos ocultos que PyInstaller puede perder
        "--hidden-import", "yt_dlp",
        "--hidden-import", "yt_dlp.extractor",
        "--hidden-import", "flet",
        "--hidden-import", "flet_core",
    ]

    # Incluir ffmpeg si está disponible en el sistema
    if ffmpeg_path:
        if SO == "Windows":
            cmd += ["--add-binary", f"{ffmpeg_path};."]
        else:
            cmd += ["--add-binary", f"{ffmpeg_path}:."]
        print(f"  📦 FFmpeg se incluirá en el paquete.")

    # Ícono (opcional)
    if os.path.exists(ICONO):
        cmd += ["--icon", ICONO]
        print(f"  🎨 Ícono: {ICONO}")
    else:
        print(f"  ℹ️  Sin ícono (coloca {ICONO} aquí para añadirlo).")

    cmd.append(SCRIPT_MAIN)

    print(f"\n  🚀 Iniciando PyInstaller…\n")
    resultado = subprocess.run(cmd, check=False)

    if resultado.returncode == 0:
        dist_path = os.path.join("dist", NOMBRE_APP)
        print(f"\n  ✅ ¡Empaquetado exitoso!")
        print(f"  📁 Ejecutable en: {os.path.abspath(dist_path)}")
        if SO == "Windows":
            exe = os.path.join(dist_path, f"{NOMBRE_APP}.exe")
            print(f"  ▶  Ejecutar: {exe}")
        else:
            exe = os.path.join(dist_path, NOMBRE_APP)
            print(f"  ▶  Ejecutar: chmod +x {exe} && {exe}")
        print()
        print("  Para distribuir: comprime la carpeta dist/ completa en un .zip")
        print("  y súbela a GitHub Releases.")
    else:
        print(f"\n  ❌ Error durante el empaquetado (código {resultado.returncode})")
        print("     Revisa los mensajes anteriores.")

if __name__ == "__main__":
    main()
