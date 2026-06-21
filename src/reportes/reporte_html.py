import os
from datetime import date
from typing import List
import pandas as pd
import plotly.express as px
from src.nucleo.modelos import RegistroDia


class GeneradorReporte:
    """
    Genera un Dashboard HTML interactivo leyendo una plantilla HTML (template.html) 
    y estilos CSS (style.css) independientes.
    """

    @staticmethod
    def generar(registros: List[RegistroDia], ruta_salida: str):
        if not registros:
            return

        # ── 1. Preparar DataFrame principal ────────────────────────────────
        filas = []
        for r in registros:
            filas.append(
                {
                    "Empleado": r.nombre,
                    "Fecha": r.fecha.strftime("%Y-%m-%d"),
                    "Horas": round(r.horas_trabajadas or 0.0, 2),
                    "Estado": "Con Novedad" if r.tiene_novedad else "Normal",
                    "Novedades": " | ".join(r.novedades) if r.novedades else "—",
                    "Entrada": r.entrada.strftime("%H:%M") if r.entrada else "FALTA",
                    "Almuerzo_ini": (
                        r.inicio_almuerzo.strftime("%H:%M")
                        if r.inicio_almuerzo
                        else "—"
                    ),
                    "Almuerzo_fin": (
                        r.fin_almuerzo.strftime("%H:%M") if r.fin_almuerzo else "—"
                    ),
                    "Salida": r.salida.strftime("%H:%M") if r.salida else "FALTA",
                }
            )
        df = pd.DataFrame(filas)

        # ── 2. Métricas resumen (KPIs) ──────────────────────────────────────
        total_empleados = df["Empleado"].nunique()
        total_dias = len(df)
        total_horas = df["Horas"].sum()
        dias_con_novedad = (df["Estado"] == "Con Novedad").sum()
        pct_novedad = round(dias_con_novedad / total_dias * 100, 1) if total_dias else 0

        # ── 3. Gráfico 1: Horas por empleado ────────────────────────────────
        horas_emp = (
            df.groupby("Empleado")["Horas"].sum().reset_index().sort_values("Horas")
        )
        fig_barras = px.bar(
            horas_emp,
            y="Empleado",
            x="Horas",
            orientation="h",
            title="Total de Horas Trabajadas por Empleado",
            labels={"Horas": "Horas totales", "Empleado": ""},
            color="Horas",
            color_continuous_scale="blues",
            text="Horas",
        )
        fig_barras.update_traces(texttemplate="%{text:.1f}h", textposition="outside")
        fig_barras.update_layout(**GeneradorReporte._layout_base())

        # ── 4. Gráfico 2: Dona de novedades ─────────────────────────────────
        conteo = df["Estado"].value_counts().reset_index()
        fig_dona = px.pie(
            conteo,
            names="Estado",
            values="count",
            title="Distribución de Días: Normal vs Con Novedad",
            color="Estado",
            color_discrete_map={"Normal": "#16a34a", "Con Novedad": "#ea580c"},
            hole=0.45,
        )
        fig_dona.update_layout(**GeneradorReporte._layout_base())

        # ── 5. Gráfico 3: Promedio de horas por fecha ───────────────────────
        horas_fecha = df.groupby("Fecha")["Horas"].mean().reset_index()
        horas_fecha.columns = ["Fecha", "Promedio_Horas"]
        fig_linea = px.line(
            horas_fecha,
            x="Fecha",
            y="Promedio_Horas",
            title="Tendencia Diaria — Promedio de Horas Trabajadas",
            markers=True,
            labels={"Promedio_Horas": "Promedio horas", "Fecha": ""},
        )
        fig_linea.update_traces(line_color="#3b82f6", marker_color="#60a5fa")
        fig_linea.update_layout(**GeneradorReporte._layout_base())

        # ── 6. Tabla HTML de novedades ───────────────────────────────────────
        df_nov = df[df["Estado"] == "Con Novedad"][
            ["Empleado", "Fecha", "Novedades", "Entrada", "Salida"]
        ]
        if df_nov.empty:
            tabla_novedades_html = "<p style='color:#22c55e;font-size:16px;'>✅ No se detectaron novedades en los registros.</p>"
        else:
            filas_html = "".join(
                f"<tr><td>{r['Empleado']}</td><td>{r['Fecha']}</td>"
                f"<td class='nov'>{r['Novedades']}</td><td>{r['Entrada']}</td><td>{r['Salida']}</td></tr>"
                for _, r in df_nov.iterrows()
            )
            tabla_novedades_html = f"""
            <table id="tabla-novedades" class="display" style="width:100%">
              <thead><tr>
                <th>Empleado</th><th>Fecha</th><th>Novedad Detectada</th><th>Entrada</th><th>Salida</th>
              </tr></thead>
              <tbody>{filas_html}</tbody>
            </table>"""

        # ── 7. Tabla HTML de resumen general ────────────────────────────────
        filas_res = "".join(
            f"<tr class='{'nov-row' if r['Estado'] == 'Con Novedad' else ''}'>"
            f"<td>{r['Empleado']}</td><td>{r['Fecha']}</td>"
            f"<td>{r['Entrada']}</td><td>{r['Almuerzo_ini']}</td>"
            f"<td>{r['Almuerzo_fin']}</td><td>{r['Salida']}</td>"
            f"<td><b>{r['Horas']:.2f}h</b></td>"
            f"<td class='estado-{'ok' if r['Estado'] == 'Normal' else 'nov'}'>"
            f"{'✅ OK' if r['Estado'] == 'Normal' else '⚠ Novedad'}</td></tr>"
            for _, r in df.iterrows()
        )

        # ── 8. Cargar plantilla HTML y CSS actualizados ─────────────────────
        ruta_directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_plantilla = os.path.join(ruta_directorio_actual, "template.html")
        ruta_css = os.path.join(ruta_directorio_actual, "style.css")

        # Verificar existencia de los nuevos archivos de diseño
        if not os.path.exists(ruta_plantilla) or not os.path.exists(ruta_css):
            raise FileNotFoundError(
                "Faltan archivos de diseño (template.html o style.css) "
                f"en el directorio: {ruta_directorio_actual}"
            )

        # Leer archivos
        with open(ruta_plantilla, "r", encoding="utf-8") as archivo:
            contenido_html = archivo.read()
        
        with open(ruta_css, "r", encoding="utf-8") as archivo:
            contenido_css = archivo.read()

        # Diccionario con los datos a inyectar en la plantilla
        reemplazos = {
            "{{ESTILOS_CSS}}": contenido_css,
            "{{FECHA_ACTUAL}}": date.today().strftime("%d/%m/%Y"),
            "{{TOTAL_EMPLEADOS}}": str(total_empleados),
            "{{TOTAL_DIAS}}": str(total_dias),
            "{{TOTAL_HORAS}}": f"{total_horas:.1f}h",
            "{{DIAS_CON_NOVEDAD}}": str(dias_con_novedad),
            "{{PCT_NOVEDAD}}": f"{pct_novedad}%",
            "{{GRAFICO_BARRAS}}": fig_barras.to_html(
                full_html=False, include_plotlyjs="cdn"
            ),
            "{{GRAFICO_DONA}}": fig_dona.to_html(
                full_html=False, include_plotlyjs=False
            ),
            "{{GRAFICO_LINEA}}": fig_linea.to_html(
                full_html=False, include_plotlyjs=False
            ),
            "{{TABLA_RESUMEN}}": filas_res,
            "{{TABLA_NOVEDADES}}": tabla_novedades_html,
        }

        # Aplicar todos los reemplazos
        for clave, valor in reemplazos.items():
            contenido_html = contenido_html.replace(clave, valor)

        # Guardar resultado final
        os.makedirs(ruta_salida, exist_ok=True)
        ruta_archivo_salida = os.path.join(ruta_salida, "reporte_grafico.html")
        with open(ruta_archivo_salida, "w", encoding="utf-8") as archivo_salida:
            archivo_salida.write(contenido_html)

    @staticmethod
    def _layout_base():
        return dict(
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font_color="#1e293b",
            margin=dict(l=20, r=20, t=44, b=20),
            height=320,
        )