import customtkinter as ctk
import os
import urllib.request
from PIL import Image

AZUL_COATS = "#003087"

class Encabezado(ctk.CTkFrame):
    """Componente que muestra el logo y título de la aplicación."""
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", corner_radius=0, height=70, **kwargs)
        self.pack_propagate(False)
        self._construir()

    def _construir(self):
        # Logo frame circular
        logo_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=50,
                                  width=54, height=54,
                                  border_width=2, border_color=AZUL_COATS)
        logo_frame.pack(side="left", padx=18, pady=8)
        logo_frame.pack_propagate(False)

        # Ruta del logo (un nivel arriba, en src/interfaz/)
        ruta_logo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png")
        if not os.path.exists(ruta_logo):
            try:
                urllib.request.urlretrieve(
                    "https://cadenacoats.com/wp-content/themes/coats/assets/img/logo.png",
                    ruta_logo)
            except Exception:
                pass

        if os.path.exists(ruta_logo):
            try:
                img = ctk.CTkImage(light_image=Image.open(ruta_logo), size=(44, 44))
                ctk.CTkLabel(logo_frame, text="", image=img,
                             fg_color="white").place(relx=0.5, rely=0.5, anchor="center")
            except Exception:
                self._logo_texto(logo_frame)
        else:
            self._logo_texto(logo_frame)

        # Título
        ctk.CTkLabel(self, text="Monitoreo de Accesos",
                     font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                     text_color=AZUL_COATS).pack(side="right", padx=24)

    def _logo_texto(self, parent):
        ctk.CTkLabel(parent, text="C", font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=AZUL_COATS).place(relx=0.5, rely=0.5, anchor="center")
