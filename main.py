import sys
from src.interfaz.app import AplicacionGUI

if __name__ == "__main__":
    try:
        # Modo Interfaz Gráfica (Punto de entrada único)
        app = AplicacionGUI()
        app.mainloop()
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: No se pudo inicializar la interfaz gráfica.")
        print(f"Detalle del fallo del entorno: {e}")
        print("Verifique que el servidor gráfico (X11/Wayland) esté activo o que disponga de un entorno de escritorio.")
        sys.exit(1)