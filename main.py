#!/usr/bin/env python3
"""
Descargador de Videos — GUI
Proyecto Ola Digital · Flet 0.84 / Python 3.12
pip install flet yt-dlp
"""

import os
import re
import shutil
import yt_dlp
import flet as ft

# ─────────────────────────────────────────────
#  UTILIDADES
# ─────────────────────────────────────────────


def ffmpeg_ok():
    return shutil.which("ffmpeg") is not None


def extraer_id(url):
    m = re.search(r'(\d{10,20})', url)
    return m.group(1) if m else None


def normalizar_url(url_raw):
    if "facebook.com" in url_raw:
        vid = extraer_id(url_raw)
        if vid:
            return f"https://www.facebook.com/watch/?v={vid}"
    return url_raw


def fmt_bytes(b):
    if b is None:
        return "?"
    for u in ['B', 'KB', 'MB', 'GB']:
        if b < 1024:
            return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} GB"


def PAD(h=0, v=0): return ft.Padding(left=h, right=h, top=v, bottom=v)
def PAD_ALL(n): return ft.Padding(left=n, top=n, right=n, bottom=n)


def BORDER(w, c):
    s = ft.BorderSide(w, c)
    return ft.Border(top=s, right=s, bottom=s, left=s)


def BORDER_ONLY(top=None, bottom=None, left=None, right=None):
    n = ft.BorderSide(0)
    return ft.Border(top=top or n, bottom=bottom or n,
                     left=left or n, right=right or n)


# ─────────────────────────────────────────────
#  PALETA OLA DIGITAL — DARK
# ─────────────────────────────────────────────
OLA = "#4ECDC4"
SURFISTA = "#E87722"
MAREA = "#2E6DA4"
D_BG = "#0F1923"
D_SURF = "#162030"
D_PANEL = "#1C2B3A"
D_CARD = "#1F3245"
D_BOR = "#2A4060"
D_TXT = "#F5F7FA"   # Espuma
D_MUT = "#D4F6F9"   # Brisa
D_HINT = "#4A6A88"
ERR = "#E05050"
BLANCO = "#FFFFFF"

# ─────────────────────────────────────────────
#  APP
# ─────────────────────────────────────────────


def main(page: ft.Page):
    page.window.resizable = True
    page.title = "Descargador de Videos"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = D_BG
    page.padding = 0

    carpeta = [os.path.join(os.path.expanduser("~"), "Downloads")]
    bajando = [False]
    listo = [False]
    es_playlist = [False]
    modo = ["1"]

    # ─────────────────────────────────────────
    #  CLAVE: refresco thread-safe
    #  page.run_task despacha la corutina al loop async de la sesión.
    #  Es la única forma correcta de actualizar UI desde un hilo externo.
    # ─────────────────────────────────────────
    async def _update():
        page.update()

    def ui():
        """Llama page.update() de forma segura desde cualquier hilo."""
        page.run_task(_update)

    # ──────────────────────────────────────────
    #  HELPERS UI
    # ──────────────────────────────────────────
    def btn_style(bg):
        return ft.ButtonStyle(
            bgcolor=bg, color=BLANCO,
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation={ft.ControlState.DEFAULT: 0, ft.ControlState.HOVERED: 6},
            animation_duration=150,
        )

    def btn_txt(label):
        return ft.Text(label, size=14, weight=ft.FontWeight.W_700,
                       color=BLANCO, no_wrap=True,
                       style=ft.TextStyle(letter_spacing=1.5))

    def sec_label(t):
        return ft.Text(t, size=10, color=D_MUT, weight=ft.FontWeight.W_600,
                       style=ft.TextStyle(letter_spacing=1.8))

    # ──────────────────────────────────────────
    #  FILEPICKER
    # ──────────────────────────────────────────
    lbl_carpeta = ft.Text(carpeta[0], size=11, color=D_MUT,
                          overflow=ft.TextOverflow.ELLIPSIS, expand=True)

    async def _pick_dir():
        ruta = await ft.FilePicker().get_directory_path()
        if ruta:
            carpeta[0] = ruta
            lbl_carpeta.value = ruta
            page.update()

    # ──────────────────────────────────────────
    #  HEADER
    # ──────────────────────────────────────────
    header = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text("▶", size=18, color=BLANCO),
                bgcolor=SURFISTA, border_radius=8,
                padding=PAD(h=10, v=7),
            ),
            ft.Column([
                ft.Text("DESCARGADOR DE VIDEOS", size=17,
                        weight=ft.FontWeight.W_800, color=OLA,
                        style=ft.TextStyle(letter_spacing=2)),
                ft.Text("YouTube · Facebook · Instagram · X · TikTok",
                        size=11, color=D_MUT),
            ], spacing=2),
        ], spacing=14),
        padding=PAD(h=24, v=16),
        border=BORDER_ONLY(bottom=ft.BorderSide(2, OLA)),
        bgcolor=D_SURF,
    )

    # ──────────────────────────────────────────
    #  URL
    # ──────────────────────────────────────────
    url_field = ft.TextField(
        hint_text="Pega el enlace aquí…",
        hint_style=ft.TextStyle(color=D_HINT, size=13),
        text_style=ft.TextStyle(color=D_TXT, size=13),
        border_color=D_BOR,
        focused_border_color=OLA,
        cursor_color=SURFISTA,
        bgcolor=D_PANEL,
        border_radius=8,
        content_padding=PAD(h=14, v=12),
        expand=True,
        prefix_icon=ft.Icons.LINK,
    )

    # ──────────────────────────────────────────
    #  PÍLDORAS
    # ──────────────────────────────────────────
    modos_cfg = [
        ("1", ft.Icons.HD,            "HD",       "Alta calidad", not ffmpeg_ok()),
        ("2", ft.Icons.PHONE_ANDROID, "WhatsApp", "Ligero 480p",  False),
        ("3", ft.Icons.MUSIC_NOTE,    "MP3",      "Solo audio", not ffmpeg_ok()),
    ]
    pills = []
    PILL_SEL = "#1A3A4A"

    def hacer_pill(val, icono, corto, desc, warn):
        def click(e, v=val):
            modo[0] = v
            for p in pills:
                sel = p.data == modo[0]
                p.border = BORDER(2, OLA if sel else D_BOR)
                p.bgcolor = PILL_SEL if sel else D_PANEL
            page.update()
        return ft.Container(
            content=ft.Column([
                ft.Icon(icono, size=22, color=OLA),
                ft.Text(corto, size=13, weight=ft.FontWeight.W_700,
                        color=D_TXT, text_align=ft.TextAlign.CENTER, no_wrap=True),
                ft.Text(desc, size=10,
                        color=D_MUT if not warn else SURFISTA,
                        text_align=ft.TextAlign.CENTER, no_wrap=True),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            width=168, height=96, border_radius=10,
            border=BORDER(2, D_BOR), bgcolor=D_PANEL,
            padding=PAD_ALL(12),
            on_click=click,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            data=val,
        )

    for m in modos_cfg:
        pills.append(hacer_pill(*m))
    pills[0].border = BORDER(2, OLA)
    pills[0].bgcolor = PILL_SEL
    pills_row = ft.Row(pills, spacing=8, alignment=ft.MainAxisAlignment.CENTER)

    # ──────────────────────────────────────────
    #  CARPETA
    # ──────────────────────────────────────────
    btn_carpeta = ft.OutlinedButton(
        content=ft.Text("ELEGIR", size=11, color=OLA, no_wrap=True,
                        style=ft.TextStyle(letter_spacing=1)),
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, OLA),
            shape=ft.RoundedRectangleBorder(radius=6),
        ),
        on_click=lambda e: page.run_task(_pick_dir),
    )
    carpeta_row = ft.Row([
        ft.Icon(ft.Icons.FOLDER_OPEN, size=16, color=D_MUT),
        lbl_carpeta, btn_carpeta,
    ], spacing=8)

    # ──────────────────────────────────────────
    #  INFO PREVIA
    # ──────────────────────────────────────────
    info_titulo = ft.Text("", size=13, color=D_TXT,
                          overflow=ft.TextOverflow.ELLIPSIS)
    info_dur = ft.Text("", size=11, color=D_MUT)
    info_tam = ft.Text("", size=11, color=D_MUT)

    info_box = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.MOVIE, size=14, color=OLA), info_titulo],
                   spacing=8),
            ft.Row([ft.Icon(ft.Icons.TIMER,      size=12, color=D_MUT), info_dur,
                    ft.Container(width=12),
                    ft.Icon(ft.Icons.DATA_USAGE, size=12, color=D_MUT), info_tam],
                   spacing=6),
        ], spacing=6),
        visible=False, bgcolor=D_CARD, border_radius=8,
        padding=PAD(h=14, v=10), border=BORDER(1, OLA),
    )

    # ──────────────────────────────────────────
    #  PLAYLIST
    # ──────────────────────────────────────────
    r_ini = ft.TextField(
        value="1", width=68, text_align=ft.TextAlign.CENTER,
        text_style=ft.TextStyle(color=D_TXT, size=13), hint_text="Desde",
        border_color=D_BOR, focused_border_color=OLA,
        bgcolor=D_PANEL, border_radius=6, content_padding=PAD(h=6, v=6),
    )
    r_fin = ft.TextField(
        value="", width=68, text_align=ft.TextAlign.CENTER,
        text_style=ft.TextStyle(color=D_TXT, size=13), hint_text="Hasta",
        border_color=D_BOR, focused_border_color=OLA,
        bgcolor=D_PANEL, border_radius=6, content_padding=PAD(h=6, v=6),
    )
    playlist_box = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.PLAYLIST_PLAY, size=16, color=OLA),
            ft.Text("Playlist — rango:", size=12, color=D_MUT),
            r_ini, ft.Text("→", color=D_MUT), r_fin,
            ft.Text("(vacío = todos)", size=10, color=D_MUT),
        ], spacing=8),
        visible=False, bgcolor=D_CARD, border_radius=8,
        padding=PAD(h=14, v=10), border=BORDER(1, D_BOR),
    )

    # ──────────────────────────────────────────
    #  PROGRESO
    # ──────────────────────────────────────────
    barra = ft.ProgressBar(value=0, color=SURFISTA, bgcolor=D_BOR,
                           border_radius=4, visible=False)
    lbl_pct = ft.Text("", size=13, color=SURFISTA, weight=ft.FontWeight.W_600)
    lbl_vel = ft.Text("", size=11, color=D_MUT)
    lbl_eta = ft.Text("", size=11, color=D_MUT)
    stats = ft.Row([lbl_pct, ft.Container(expand=True),
                    lbl_vel, ft.Text("·", color=D_MUT), lbl_eta],
                   visible=False)
    estado = ft.Text("", size=12, color=D_MUT, text_align=ft.TextAlign.CENTER)

    aviso_ff = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.WARNING_AMBER, size=14, color=SURFISTA),
            ft.Text("FFmpeg no detectado — HD y MP3 pueden fallar",
                    size=11, color=D_TXT),
        ], spacing=6),
        visible=not ffmpeg_ok(),
        bgcolor="#2A1A0A", border_radius=6,
        padding=PAD(h=12, v=6), border=BORDER(1, "#5A3A10"),
    )

    btn = ft.Button(
        content=btn_txt("DESCARGAR"),
        bgcolor=SURFISTA, style=btn_style(SURFISTA),
        height=52, expand=True,
    )

    # ──────────────────────────────────────────
    #  RESET — limpia todo para nueva descarga
    # ──────────────────────────────────────────
    def reset_ui(limpiar_url=False):
        listo[0] = False
        bajando[0] = False
        btn.disabled = False
        btn.content = btn_txt("DESCARGAR")
        btn.bgcolor = SURFISTA
        btn.style = btn_style(SURFISTA)
        barra.value = 0
        barra.color = SURFISTA
        barra.visible = False
        stats.visible = False
        lbl_pct.value = lbl_vel.value = lbl_eta.value = ""
        estado.value = ""
        estado.color = D_MUT
        if limpiar_url:
            url_field.value = ""
            info_titulo.value = ""
            info_dur.value = ""
            info_tam.value = ""
            info_box.visible = False
            playlist_box.visible = False
        page.update()

    # ──────────────────────────────────────────
    #  LÓGICA DE DESCARGA
    #  Toda actualización de UI usa ui() = page.run_task(_update)
    #  que despacha page.update() al loop async de la sesión
    # ──────────────────────────────────────────
    def set_estado(msg, color=None):
        estado.value = msg
        if color:
            estado.color = color
        ui()

    def hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            dl = d.get('downloaded_bytes', 0)
            vel = d.get('speed')
            eta = d.get('eta')
            if total:
                pct = dl / total
                barra.value = pct
                lbl_pct.value = f"{pct*100:.1f}%"
            else:
                barra.value = None
            lbl_vel.value = f"{fmt_bytes(vel)}/s" if vel else "---"
            lbl_eta.value = f"ETA {eta}s" if eta else ""
            ui()
        elif d['status'] == 'finished':
            set_estado("⚙ Procesando…", D_MUT)
        elif d['status'] == 'error':
            set_estado("Error en fragmento", ERR)

    def obtener_info(url, opts_base):
        opts = {**opts_base, 'quiet': True, 'no_warnings': True,
                'progress_hooks': []}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                titulo = info.get('title', 'Sin título')
                dur = info.get('duration')
                entries = info.get('entries')
                if entries:
                    total = len(list(entries))
                    info_titulo.value = f"Playlist: {titulo}"
                    info_dur.value = f"{total} videos"
                    info_tam.value = ""
                    es_playlist[0] = True
                    playlist_box.visible = True
                else:
                    tam = info.get('filesize') or info.get('filesize_approx')
                    ds = f"{dur//60}:{dur % 60:02d}" if dur else "--:--"
                    info_titulo.value = titulo
                    info_dur.value = ds
                    info_tam.value = fmt_bytes(tam)
                    es_playlist[0] = False
                    playlist_box.visible = False
                info_box.visible = True
                ui()
        except Exception as ex:
            set_estado(f"Info no disponible: {ex}", D_MUT)

    async def descarga_async():
        """Corutina principal de descarga — corre en el loop async de la sesión."""
        import asyncio

        bajando[0] = True
        listo[0] = False
        btn.disabled = True
        btn.content = btn_txt("DESCARGANDO…")
        btn.bgcolor = MAREA
        btn.style = btn_style(MAREA)
        barra.visible = True
        barra.value = 0
        barra.color = SURFISTA
        stats.visible = True
        page.update()

        url_raw = (url_field.value or "").strip()
        if not url_raw:
            set_estado("Pega un enlace primero.", ERR)
            reset_ui()
            return

        url = normalizar_url(url_raw)
        dest = carpeta[0]
        os.makedirs(dest, exist_ok=True)

        m = modo[0]
        if m == "2":
            tag = "[WA]"
            fmt = "bestvideo[height<=480][vcodec^=avc]+bestaudio/best[height<=480]/best"
            post = []
        elif m == "3":
            tag = "[MP3]"
            fmt = "bestaudio/best"
            post = [{'key': 'FFmpegExtractAudio',
                     'preferredcodec': 'mp3', 'preferredquality': '192'}]
        else:
            tag = "[HD]"
            fmt = "bestvideo+bestaudio/best"
            post = []

        ydl_opts = {
            'format':              fmt,
            'outtmpl':             os.path.join(dest, f'%(title)s {tag}.%(ext)s'),
            'nocheckcertificate':  True,
            'merge_output_format': 'mp4',
            'progress_hooks':      [hook],
            'postprocessors':      post,
            'quiet':               True,
            'no_warnings':         False,
            'extractor_args': {
                'youtube':  {'player_client': ['web', 'android'],
                             'player_skip':   ['webpage', 'configs']},
                'facebook': {'rewrite_display_id': True},
            },
        }

        cookie_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "cookies.txt")
        if os.path.exists(cookie_path):
            ydl_opts['cookiefile'] = cookie_path

        set_estado("Obteniendo información…", D_MUT)
        # obtener_info es bloqueante — lo corremos en executor para no bloquear el loop
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, obtener_info, url, ydl_opts)

        if es_playlist[0]:
            ini = r_ini.value.strip()
            fin = r_fin.value.strip()
            if ini and fin:
                ydl_opts['playlist_items'] = f"{ini}-{fin}"
            elif ini:
                ydl_opts['playlist_items'] = f"{ini}-"

        try:
            set_estado(f"Descargando {tag}…", D_MUT)
            with yt_dlp.YoutubeDL({'quiet': True}) as yc:
                yc.cache.remove()
            # yt-dlp es bloqueante — executor para no congelar el loop
            await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).download([url])
            )

            barra.value = 1.0
            barra.color = OLA
            lbl_pct.value = "100%"
            lbl_vel.value = lbl_eta.value = ""
            estado.value = f"✓ Guardado en: {dest}"
            estado.color = OLA
            btn.content = btn_txt("✓ LISTO  —  clic para nueva descarga")
            btn.bgcolor = OLA
            btn.style = btn_style(OLA)
            btn.disabled = False
            listo[0] = True
            bajando[0] = False

        except Exception as ex:
            estado.value = f"✗ {ex}"
            estado.color = ERR
            btn.content = btn_txt("REINTENTAR")
            btn.bgcolor = ERR
            btn.style = btn_style(ERR)
            btn.disabled = False
            listo[0] = False
            bajando[0] = False

        finally:
            page.update()

    def on_descargar(e):
        if bajando[0]:
            return
        if listo[0]:
            # Limpiar URL y estado, listo para nueva descarga
            reset_ui(limpiar_url=True)
            return
        # page.run_task despacha descarga_async al loop async de la sesión
        page.run_task(descarga_async)

    def on_limpiar(e):
        if not bajando[0]:
            reset_ui(limpiar_url=True)

    btn.on_click = on_descargar

    btn_limpiar = ft.IconButton(
        icon=ft.Icons.CLOSE, icon_color=D_MUT, icon_size=18,
        tooltip="Limpiar", on_click=on_limpiar,
    )

    # ──────────────────────────────────────────
    #  LAYOUT
    # ──────────────────────────────────────────
    def sec(titulo, widget):
        return ft.Column([sec_label(titulo), widget], spacing=8)

    cuerpo = ft.Container(
        content=ft.Column([
            sec("ENLACE",  ft.Row([url_field, btn_limpiar], spacing=8)),
            sec("FORMATO", pills_row),
            sec("DESTINO", carpeta_row),
            aviso_ff,
            info_box,
            playlist_box,
            ft.Divider(height=1, color=D_BOR),
            ft.Row([btn]),
            barra,
            stats,
            ft.Container(content=estado, alignment=ft.Alignment(0, 0)),
        ], spacing=16),
        padding=PAD(h=26, v=22),
        expand=True, bgcolor=D_BG,
    )

    footer = ft.Container(
        content=ft.Row([
            ft.Text("cookies.txt en la misma carpeta para contenido privado",
                    size=10, color=D_MUT),
            ft.Container(expand=True),
            ft.Text("yt-dlp · Ola Digital", size=10, color=D_MUT),
        ]),
        padding=PAD(h=26, v=10),
        border=BORDER_ONLY(top=ft.BorderSide(2, OLA)),
        bgcolor=D_SURF,
    )

    page.add(ft.Column([
        header,
        ft.Container(content=cuerpo, expand=True),
        footer,
    ], expand=True, spacing=0))

    # Mostrar ventana centrada ahora que el contenido está listo
    page.window.visible = True
    page.run_task(page.window.center)
    page.update()


def before_main(page: ft.Page):
    """Se ejecuta antes de main — configura ventana lo antes posible."""
    page.window.width = 560
    page.window.height = 700
    page.window.min_width = 520
    page.window.min_height = 640
    page.window.bgcolor = "#0F1923"
    page.bgcolor = "#0F1923"


if __name__ == "__main__":
    ft.run(main, before_main=before_main, view=ft.AppView.FLET_APP_HIDDEN)
