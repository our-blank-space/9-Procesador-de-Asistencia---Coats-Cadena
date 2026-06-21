import customtkinter as ctk

class TarjetaKPI(ctk.CTkFrame):
    """Tarjeta reutilizable que muestra un indicador numérico con su etiqueta."""

    def __init__(self, master, titulo: str, valor: str, color: str, **kwargs):
        super().__init__(master,
                         fg_color="white",
                         corner_radius=14,
                         border_width=2,
                         border_color=color,
                         **kwargs)
        ctk.CTkLabel(self,
                     text=titulo.upper(),
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=color).pack(pady=(10, 0))

        self._lbl_valor = ctk.CTkLabel(self,
                                       text=valor,
                                       font=ctk.CTkFont(size=30, weight="bold"),
                                       text_color=color)
        self._lbl_valor.pack(pady=(0, 10))

    def actualizar(self, nuevo_valor: str):
        self._lbl_valor.configure(text=nuevo_valor)
