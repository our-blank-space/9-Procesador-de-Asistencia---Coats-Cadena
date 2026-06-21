import customtkinter as ctk
from tkinter import messagebox
import os
import threading
import webbrowser

from src.archivos.lector_excel import LectorExcel
from src.nucleo.procesador import ProcesadorAsistencia
from src.archivos.escritor_excel import EscritorExcel
from src.reportes.reporte_html import GeneradorReporte

# Importar Componentes Modulares
from src.interfaz.componentes.encabezado import Encabezado
from src.interfaz.componentes.zona_carga import ZonaCarga
from src.interfaz.componentes.tarjeta_kpi import TarjetaKPI
#from src.interfaz.vista_dashboard import VistaDashboard

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ── Paleta de colores Coats Cadena ────────────────────────────────────────────
AZUL_COATS  = "#003087"
AZUL_ACENTO = "#2563eb"
VERDE_OK    = "#16a34a"
NARANJA_AVS = "#ea580c"
MORADO      = "#7c3aed"


# ══════════════════════════════════════════════════════════════════════════════
# Ventana Principal — Orquestador
# ══════════════════════════════════════════════════════════════════════════════
class AplicacionGUI(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Monitoreo de Accesos — Coats Cadena")
        self.geometry("800x580")
        self.resizable(False, False)
        self.configure(fg_color="white")

        self.ruta_archivo    = None
        self.registros       = []
        self._carpeta_salida = None
        self._resumen_datos  = {}

        self._construir_ui()

    # ── Construcción de la interfaz ───────────────────────────────────────────
    def _construir_ui(self):
        # 1. Encabezado (Modular)
        self.encabezado = Encabezado(self)
        self.encabezado.pack(fill="x")

        # Línea separadora
        ctk.CTkFrame(self, fg_color=AZUL_ACENTO, corner_radius=0, height=3).pack(fill="x")

        # 2. Zona de carga (Modular)
        self.zona_carga = ZonaCarga(self, al_seleccionar=self._en_archivo_listo)
        self.zona_carga.pack(fill="x", padx=24, pady=(20, 8))

        # 3. Botón Procesar
        self.btn_procesar = ctk.CTkButton(self,
                                          text="  ▶▶  Procesar y Generar Reportes",
                                          command=self._iniciar_procesamiento,
                                          state="disabled",
                                          height=50,
                                          font=ctk.CTkFont(size=15, weight="bold"),
                                          fg_color=AZUL_COATS,
                                          hover_color="#001a4d",
                                          text_color="white",
                                          corner_radius=10)
        self.btn_procesar.pack(fill="x", padx=24, pady=(0, 6))

        # 4. Barra de carga
        self.barra = ctk.CTkProgressBar(self, height=6, fg_color="#e2e8f0",
                                        progress_color=AZUL_ACENTO)
        self.barra.pack(fill="x", padx=24, pady=(0, 4))
        self.barra.set(0)

        self.lbl_estado = ctk.CTkLabel(self, text="", text_color="#64748b", font=ctk.CTkFont(size=11))
        self.lbl_estado.pack(anchor="w", padx=26)

        # 5. Análisis General (KPIs) (Modulares)
        ctk.CTkLabel(self, text="Análisis General",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#64748b").pack(anchor="w", padx=26, pady=(12, 4))

        marco_kpi = ctk.CTkFrame(self, fg_color="transparent")
        marco_kpi.pack(fill="x", padx=24, pady=(0, 16))

        self.kpi_empleados = TarjetaKPI(marco_kpi, "Empleados", "—", AZUL_ACENTO)
        self.kpi_empleados.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.kpi_dias = TarjetaKPI(marco_kpi, "Días Procesados", "—", MORADO)
        self.kpi_dias.pack(side="left", expand=True, fill="x", padx=6)

        self.kpi_horas = TarjetaKPI(marco_kpi, "Total Horas", "—", VERDE_OK)
        self.kpi_horas.pack(side="left", expand=True, fill="x", padx=6)

        self.kpi_novedades = TarjetaKPI(marco_kpi, "Con Novedad", "—", NARANJA_AVS)
        self.kpi_novedades.pack(side="left", expand=True, fill="x", padx=(6, 0))

        # 6. Botones de acción
        zona_acc = ctk.CTkFrame(self, fg_color="transparent")
        zona_acc.pack(fill="x", padx=24, pady=(0, 24))

        self.btn_excel = ctk.CTkButton(zona_acc, text="📊  Abrir Excel Resumen",
                                       command=self._abrir_excel, state="disabled", height=40,
                                       fg_color="#f1f5f9", hover_color="#e2e8f0", text_color=AZUL_COATS,
                                       border_width=1, border_color="#cbd5e1", font=ctk.CTkFont(size=12))
        self.btn_excel.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.btn_html = ctk.CTkButton(zona_acc, text="🖥  Ver Dashboard",
                                      command=self._abrir_navegador, state="disabled", height=40,
                                      fg_color="#f1f5f9", hover_color="#e2e8f0", text_color=AZUL_COATS,
                                      border_width=1, border_color="#cbd5e1", font=ctk.CTkFont(size=12))
        self.btn_html.pack(side="left", expand=True, fill="x", padx=6)

        self.btn_pdf = ctk.CTkButton(zona_acc, text="📄  Exportar PDF",
                                     command=self._exportar_pdf, state="disabled", height=40,
                                     fg_color="#f1f5f9", hover_color="#e2e8f0", text_color=AZUL_COATS,
                                     border_width=1, border_color="#cbd5e1", font=ctk.CTkFont(size=12))
        self.btn_pdf.pack(side="left", expand=True, fill="x", padx=(6, 0))

    # ── Acciones (Controlador) ────────────────────────────────────────────────
    def _en_archivo_listo(self, ruta: str):
        """Callback llamado por ZonaCarga cuando el usuario elige un archivo."""
        self.ruta_archivo = ruta
        self.btn_procesar.configure(state="normal")

    def _iniciar_procesamiento(self):
        self.btn_procesar.configure(state="disabled", text="⏳  Procesando…")
        self.barra.configure(mode="indeterminate")
        self.barra.start()
        threading.Thread(target=self._procesar, daemon=True).start()

    def _procesar(self):
        try:
            carpeta = os.path.join(os.path.dirname(self.ruta_archivo), "RESULTADOS_ASISTENCIA")
            self._set_estado("Leyendo archivo…")
            marcaciones = LectorExcel.leer_marcaciones(self.ruta_archivo)
            
            self._set_estado("Calculando horas y detectando inconsistencias…")
            self.registros = ProcesadorAsistencia().procesar(marcaciones)
            
            self._set_estado("Exportando archivos…")
            EscritorExcel.generar_reportes(self.registros, carpeta)
            GeneradorReporte.generar(self.registros, carpeta)

            self._carpeta_salida = carpeta
            self._resumen_datos = {
                "empleados": len({r.empleado_id for r in self.registros}),
                "dias":      len(self.registros),
                "horas":     sum(r.horas_trabajadas or 0 for r in self.registros),
                "novedades": sum(1 for r in self.registros if r.tiene_novedad),
            }
            self._actualizar_kpis()
            self._set_estado("✔  Proceso completado exitosamente", VERDE_OK)

            self.btn_excel.configure(state="normal")
            self.btn_html.configure(state="normal")
            self.btn_pdf.configure(state="normal")

        except Exception as e:
            self._set_estado(f"✖  Error: {str(e)}", NARANJA_AVS)
            messagebox.showerror("Error", str(e))
        finally:
            self.barra.stop()
            self.barra.configure(mode="determinate")
            self.barra.set(1)
            self.btn_procesar.configure(state="normal", text="  ▶▶  Procesar y Generar Reportes")

    def _actualizar_kpis(self):
        d = self._resumen_datos
        self.kpi_empleados.actualizar(str(d["empleados"]))
        self.kpi_dias.actualizar(str(d["dias"]))
        self.kpi_horas.actualizar(f"{d['horas']:.0f}h")
        pct = round(d["novedades"] / d["dias"] * 100) if d["dias"] else 0
        self.kpi_novedades.actualizar(f"{d['novedades']}  {pct}%")

    def _set_estado(self, texto: str, color: str = "#64748b"):
        self.lbl_estado.configure(text=texto, text_color=color)
        self.update_idletasks()

    def _abrir_excel(self):
        ruta = os.path.join(self._carpeta_salida, "resumen_asistencia.xlsx")
        if os.path.exists(ruta):
            os.system(f'xdg-open "{ruta}"')

    def _abrir_navegador(self):
        if self._carpeta_salida:
            ruta_html = os.path.join(self._carpeta_salida, "reporte_grafico.html")
            if os.path.exists(ruta_html):
                import pathlib
                url = pathlib.Path(ruta_html).resolve().as_uri()
                webbrowser.open(url)
            else:
                messagebox.showwarning("Aviso", "No se encontró el archivo 'reporte_grafico.html' en la carpeta de resultados.")
        else:
            messagebox.showwarning("Aviso", "El reporte aún no se ha generado.")

    def _exportar_pdf(self):
        messagebox.showinfo("Próximamente", "La exportación a PDF estará disponible en la próxima versión.")