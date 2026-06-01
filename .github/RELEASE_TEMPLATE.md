# Descargador de Videos v1.0.1 - Windows & Linux

## ✅ Mejoras en esta versión

### 🐛 Correcciones:
- Arreglado error de descarga en Facebook ("File name too long")
- Optimización de compatibilidad multi-plataforma

### ✨ Características principales:
- ✅ Soporte multi-plataforma: YouTube, Facebook, Instagram, X (Twitter), TikTok
- ✅ Múltiples formatos de descarga:
  - **HD** - Máxima calidad disponible
  - **WhatsApp** - 480p, ligero para compartir
  - **MP3** - Solo audio (192kbps)

---

## 📥 Descarga e instalación

### Windows
1. Descarga `DescargadorVideos_Windows.zip`
2. Descomprime (clic derecho → Extraer todo)
3. Abre la carpeta y haz doble clic en `DescargadorVideos.exe`

**Sin necesidad de instalar Python. Todo incluido.**

### Linux
1. Descarga `DescargadorVideos_Linux.zip`
2. Descomprime: `unzip DescargadorVideos_Linux.zip`
3. Ejecuta: `./DescargadorVideos`

**Sin necesidad de instalar Python. Todo incluido.**

---

<details>
<summary>🔒 <strong>Verificar autenticidad del archivo (Avanzado)</strong></summary>

### ¿Por qué verificar?
Para confirmarte que el archivo no ha sido modificado o dañado durante la descarga.

### SHA256 checksums:

```
Windows:
DescargadorVideos_Windows.zip
[REEMPLAZA_CON_SHA256_REAL]

Linux:
DescargadorVideos_Linux.zip
[REEMPLAZA_CON_SHA256_REAL]
```

### Cómo verificar:

#### 🪟 Windows (PowerShell):
1. Abre **PowerShell** (tecla Windows + X → Windows PowerShell)
2. Ve a la carpeta donde descargaste el archivo:
   ```powershell
   cd "C:\Users\TuUsuario\Downloads"
   ```
3. Ejecuta:
   ```powershell
   certUtil -hashfile DescargadorVideos_Windows.zip SHA256
   ```
4. Compara el resultado con el SHA256 de arriba

#### 🐧 Linux / Mac (Terminal):
1. Abre la terminal
2. Ve a la carpeta donde descargaste el archivo:
   ```bash
   cd ~/Downloads
   ```
3. Ejecuta:
   ```bash
   sha256sum DescargadorVideos_Linux.zip
   ```
   o
   ```bash
   shasum -a 256 DescargadorVideos_Linux.zip
   ```
4. Compara el resultado con el SHA256 de arriba

**Si los valores coinciden: ✅ El archivo es auténtico**

</details>

---

## 🚀 Primeros pasos

1. Descarga la versión para tu sistema
2. Descomprime
3. Ejecuta el programa
4. ¡Listo! Pega la URL del video que quieres descargar

## 📞 Soporte

¿Problemas? Abre un [issue](https://github.com/JoseRojasProg/descargador_gui/issues)
