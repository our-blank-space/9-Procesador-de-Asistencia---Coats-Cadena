import customtkinter as ctk
from tkinter import filedialog
import os
from typing import Callable

AZUL_ACENTO = "#2563eb"
VERDE_OK    = "#16a34a"

class ZonaCarga(ctk.CTkFrame):
    """Componente visual para seleccionar el archivo de marcaciones."""
    
    def __init__(self, master, al_seleccionar: Callable[[str], None], **kwargs):
        super().__init__(master, fg_color="#f8fafc", corner_radius=12,
                         border_width=1, border_color="#e2e8f0", **kwargs)
        self._al_seleccionar = al_seleccionar
        self._construir()

    def _construir(self):
        ctk.CTkLabel(self, text="Archivo de marcaciones",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#334155").pack(anchor="w", padx=16, pady=(12, 6))

        fila = ctk.CTkFrame(self, fg_color="transparent")
        fila.pack(fill="x", padx=16, pady=(0, 12))

        self.btn_cargar = ctk.CTkButton(fila,
                                        text="🗂  Seleccionar Excel .xls .xlsx",
                                        command=self._abrir_dialogo,
                                        width=250, height=36,
                                        fg_color=AZUL_ACENTO, hover_color="#1d4ed8",
                                        font=ctk.CTkFont(size=12))
        self.btn_cargar.pack(side="left")

        self.lbl_archivo = ctk.CTkLabel(fila,
                                        text="Ningún archivo seleccionado",
                                        text_color="#94a3b8",
                                        font=ctk.CTkFont(size=12))
        self.lbl_archivo.pack(side="left", padx=16)

    def _abrir_dialogo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de marcaciones",
            filetypes=[("Archivos Excel", "*.xls *.xlsx")]
        )
        if ruta:
            nombre = os.path.basename(ruta)
            self.lbl_archivo.configure(text=f"✅  {nombre}", text_color=VERDE_OK)
            self._al_seleccionar(ruta)
