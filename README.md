<!-- BANNER DE PROMOCIÓN DEL CANAL -->
> ### 🌊 ¡Únete a nuestro canal de Telegram!
> **Proyecto Ola Digital** es una iniciativa para potenciar el aprendizaje técnico y el software libre.
> 📢 **[¡Haz clic aquí para unirte al Canal de Telegram!](https://t.me/ProyectoOlaDigital)**
> 📦 *Descarga los ejecutables portátiles listos para usar en Windows y Linux sin necesidad de compilar código ni instalar dependencias.*

---

# Descargador de Videos — GUI

Descargador de videos con interfaz gráfica para **Windows y Linux**.
Soporta YouTube, Facebook, Instagram, X (Twitter) y TikTok.

Proyecto Ola Digital · Flet 0.84 / Python 3.12

## Requisitos para desarrolladores

```bash
pip install flet yt-dlp
```

FFmpeg (para modo HD y MP3):
- **Windows**: descarga de https://ffmpeg.org/download.html → coloca `ffmpeg.exe` en PATH
- **Linux**: `sudo apt install ffmpeg` o `sudo dnf install ffmpeg`

## Ejecutar en modo desarrollo

```bash
python main.py
```

## Generar ejecutable portable

```bash
python empaquetar.py
```

El ejecutable queda en `dist/DescargadorVideos/`.
Comprime esa carpeta en `.zip` para distribuir.

## Distribución en GitHub

1. Crear repositorio en GitHub
2. Subir el código fuente (`main.py`, `empaquetar.py`, `README.md`)
3. Generar el ejecutable en Windows y en Linux
4. Ir a **Releases → New release**
5. Subir los dos `.zip` como assets de la release
6. El usuario descarga, descomprime y ejecuta — **sin instalar Python**

## Modos de descarga

| Modo | Descripción | Requiere FFmpeg |
|------|-------------|-----------------|
| HD | Máxima calidad disponible | Sí |
| WhatsApp | H.264, máx 480p, ligero | No |
| MP3 | Solo audio en mp3 192kbps | Sí |

## cookies.txt (contenido privado)

Para descargar videos privados (Instagram, Facebook), coloca un archivo
`cookies.txt` en la misma carpeta que el ejecutable. La app lo detecta
automáticamente.

Extensión recomendada para exportar cookies: **Get cookies.txt LOCALLY**

## Estructura del proyecto

```
descargador_gui/
├── main.py          ← App principal (Flet)
├── empaquetar.py    ← Script de empaquetado
├── README.md
├── cookies.txt      ← Opcional, no subir a GitHub
└── icon.ico         ← Opcional, ícono del ejecutable
```

## Compartir por WhatsApp

Una vez generado el `.zip`:
1. Súbelo a GitHub Releases (enlace directo de descarga)
2. Comparte el enlace de la release por WhatsApp
3. El usuario descarga, descomprime, doble clic en el `.exe`

> El `.zip` de Windows suele pesar entre 40-80 MB por las dependencias de Flet.
> Demasiado grande para enviar directamente por WhatsApp — el enlace de GitHub
> es la forma correcta.
