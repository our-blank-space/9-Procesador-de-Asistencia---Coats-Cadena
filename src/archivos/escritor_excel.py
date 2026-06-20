import pandas as pd 
import os
from typing import List
from src.nucleo.modelos import RegistroDia

class EscritorEkcel:
    """
    Toma los resultados procesados por el cerebro 
    (modelos.py) y los exporta a archivos Ecxel. 
    Generara dos tablas:
    1- Resumen de horas
    2- Reporte de inconsistencias 
    """

    @staticmethod
    def generar_reportes(registros: List[RegistroDia], carpeta_salida: str):
        # Asegurarnos de que la carpeta de salida exista
        os.makedirs(carpeta_salida, exist_ok=True)
        filas_resumen = []
        filas_novedades = []
        for r in registros:
            # Construir la fila para el Resumen General
            filas_resumen.append({
                "Empleado": r.nombre,
                "Fecha": r.fecha.strftime("%Y-%m-%d"),
                "Entrada": r.entrada.strftime("%H:%M") if r.entrada else "—",
                "Inicio Almuerzo": r.inicio_almuerzo.strftime("%H:%M") if r.inicio_almuerzo else "—",
                "Fin Almuerzo": r.fin_almuerzo.strftime("%H:%M") if r.fin_almuerzo else "—",
                "Salida": r.salida.strftime("%H:%M") if r.salida else "—",
                "Horas Trabajadas": round(r.horas_trabajadas, 2) if r.horas_trabajadas else 0.0,
                "Estado": "⚠ Novedad" if r.tiene_novedad else "✅ OK"
            })
            # Si el día tuvo un problema, lo enviamos al reporte de Novedades
            if r.tiene_novedad:
                for nov in r.novedades:
                    filas_novedades.append({
                        "Empleado": r.nombre,
                        "Fecha": r.fecha.strftime("%Y-%m-%d"),
                        "Error / Excepción": nov
                    })
        # Convertir nuestras listas a DataFrames (Tablas de Pandas)
        df_resumen = pd.DataFrame(filas_resumen)
        df_novedades = pd.DataFrame(filas_novedades)
        # Exportar físicamente al disco duro
        ruta_resumen = os.path.join(carpeta_salida, "resumen_asistencia.xlsx")
        df_resumen.to_excel(ruta_resumen, index=False)
        # Solo exportar novedades si existen errores
        if not df_novedades.empty:
            ruta_nov = os.path.join(carpeta_salida, "novedades_excepciones.xlsx")
            df_novedades.to_excel(ruta_nov, index=False)