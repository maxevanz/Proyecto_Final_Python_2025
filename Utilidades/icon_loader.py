from pathlib import Path
from PIL import Image, ImageTk

# Carpeta de íconos (ajustá si cambia la estructura)
ICON_DIR = Path(__file__).resolve().parent / "icon"

def cargar_icono(nombre_archivo: str, size=(24, 24)) -> ImageTk.PhotoImage:
    """
    Carga un ícono PNG desde la carpeta de iconos y lo escala al tamaño indicado.
    Devuelve un objeto PhotoImage listo para usar en Tkinter.
    """
    ruta = ICON_DIR / nombre_archivo
    if not ruta.exists():
        print(f"[ERROR] No se encontró el ícono: {ruta}")
        return ImageTk.PhotoImage(Image.new("RGBA", size, (0, 0, 0, 0)))  # ícono transparente placeholder
    
    img = Image.open(ruta).resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)
