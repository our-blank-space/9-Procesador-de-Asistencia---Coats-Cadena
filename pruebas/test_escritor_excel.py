import os
import pytest
import pandas as pd
from datetime import date, time
from src.nucleo.modelos import RegistroDia
from src.archivos.escritor_excel import EscritorExcel

# ── Fixture: Generamos datos de mentira en la memoria ──
@pytest.fixture
def registros_prueba():
    """Genera 2 registros de prueba: uno perfecto y uno con error."""
    r1 = RegistroDia(
        empleado_id="E01", nombre="Juan", fecha=date(2026, 6, 8),
        entrada=time(6, 0), inicio_almuerzo=time(12, 0),
        fin_almuerzo=time(13, 0), salida=time(16, 0),
        horas_trabajadas=9.0, tiene_novedad=False
    )
    r2 = RegistroDia(
        empleado_id="E02", nombre="Ana", fecha=date(2026, 6, 8),
        tiene_novedad=True, novedades=["EX-003: Sin salida final detectada"]
    )
    return [r1, r2]

# ── Prueba 1: Verificar que se crean los archivos ──
def test_escritor_crea_archivos(registros_prueba, tmp_path):
    """Verifica que el escritor genere físicamente los archivos .xlsx."""
    carpeta_temporal = str(tmp_path)
    
    # Mandamos a escribir a la carpeta fantasma
    EscritorExcel.generar_reportes(registros_prueba, carpeta_temporal)
    
    ruta_resumen = os.path.join(carpeta_temporal, "resumen_asistencia.xlsx")
    ruta_nov = os.path.join(carpeta_temporal, "novedades_excepciones.xlsx")
    
    # Assert revisa que los archivos sí existan
    assert os.path.exists(ruta_resumen)
    assert os.path.exists(ruta_nov)

# ── Prueba 2: Verificar que Excel dice la verdad ──
def test_escritor_datos_resumen_correctos(registros_prueba, tmp_path):
    """Verifica que los datos exportados en el resumen sean exactos."""
    carpeta = str(tmp_path)
    EscritorExcel.generar_reportes(registros_prueba, carpeta)
    
    ruta_resumen = os.path.join(carpeta, "resumen_asistencia.xlsx")
    # Pandas vuelve a abrir el excel que acabamos de crear para leerlo
    df = pd.read_excel(ruta_resumen)
    
    assert len(df) == 2  # Debe tener 2 filas
    assert df.iloc[0]["Empleado"] == "Juan"
    assert df.iloc[0]["Horas Trabajadas"] == 9.0
    assert df.iloc[1]["Estado"] == "⚠ Novedad"
