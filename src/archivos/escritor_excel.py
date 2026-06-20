import pandas as pd
import os
from typing import List
from src.nucleo.modelos import RegistroDia

class EscritorExcel:
    """
    Toma los resultados procesados por el Cerebro y los exporta a archivos Excel.
    """
    @staticmethod
    def generar_reportes(registros: List[RegistroDia], carpeta_salida: str):
        # AQUÍ CREAMOS LA CARPETA SI NO EXISTE
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

            # Novedades / Errores
            if r.tiene_novedad:
                for nov in r.novedades:
                    filas_novedades.append({
                        "Empleado": r.nombre,
                        "Fecha": r.fecha.strftime("%Y-%m-%d"),
                        "Error / Excepción": nov
                    })

        df_resumen = pd.DataFrame(filas_resumen)
        df_novedades = pd.DataFrame(filas_novedades)

        ruta_resumen = os.path.join(carpeta_salida, "resumen_asistencia.xlsx")
        df_resumen.to_excel(ruta_resumen, index=False)

        if not df_novedades.empty:
            ruta_nov = os.path.join(carpeta_salida, "novedades_excepciones.xlsx")
            df_novedades.to_excel(ruta_nov, index=False)


"""

# ==========================================
# BLOQUE DE PRUEBA: TUBERÍA COMPLETA
# ==========================================
if __name__ == '__main__':
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    
    from src.archivos.lector_excel import LectorExcel
    from src.nucleo.procesador import ProcesadorAsistencia
    
    print("Iniciando prueba de la tubería completa...")
    
    # Tu ruta donde sí funcionó:
    ruta_entrada = "Data.xls" 
    carpeta_salida = "RESULTADOS_PRUEBA"
    
    try:
        print("1. Lector: Extrayendo datos del Excel crudo...")
        marcas_crudas = LectorExcel.leer_marcaciones(ruta_entrada)
        
        print("2. Cerebro: Analizando matemáticas y buscando novedades...")
        cerebro = ProcesadorAsistencia()
        registros_finales = cerebro.procesar(marcas_crudas)
        
        print(f"3. Escritor: Creando nuevos archivos Excel en {carpeta_salida}...")
        EscritorExcel.generar_reportes(registros_finales, carpeta_salida)
        
        print("\n✅ ¡ÉXITO TOTAL! Revisa tus carpetas, debes tener dos archivos Excel.")
        
    except Exception as e:
        print(f"Uy, algo falló: {e}")

"""
