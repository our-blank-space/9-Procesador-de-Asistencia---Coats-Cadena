import os
import pytest
import pandas as pd
from src.archivos.lector_excel import LectorExcel

# ── Fixture: crea un Excel falso antes de cada prueba y lo borra al terminar ──
@pytest.fixture
def excel_prueba(tmp_path):
    """Genera un archivo Excel temporal con datos de prueba controlados."""
    datos = {
        "ID": ["EMP001", "EMP002", "EMP003"],
        "fecha": ["2026-06-08", "2026-06-08", "2026-06-08"],
        "# de registros": [4, 2, 1],
        "Hora mas temprana": ["06:00:00", "07:00:00", "08:00:00"],
        "última Hora": ["16:00:00", "15:00:00", "08:00:00"],
        # EMP001: día perfecto con 4 marcas
        # EMP002: día incompleto con 2 marcas
        # EMP003: solo entró, 1 marca
        "Hora de Registro": [
            "06:00:00;12:00:00;13:00:00;16:00:00",
            "07:00:00;15:00:00",
            "08:00:00"
        ]
    }
    ruta = tmp_path / "marcaciones_prueba.xlsx"
    pd.DataFrame(datos).to_excel(ruta, index=False)
    return str(ruta)


# ── Prueba 1: El lector lee las filas y genera marcaciones ──────────────────
def test_lector_retorna_marcaciones(excel_prueba):
    """Verifica que el lector extrae marcaciones desde el Excel."""
    marcaciones = LectorExcel.leer_marcaciones(excel_prueba)
    # EMP001 tiene 4 marcas + EMP002 tiene 2 + EMP003 tiene 1 = 7 en total
    assert len(marcaciones) == 7


# ── Prueba 2: Cada marcación tiene el ID correcto ───────────────────────────
def test_marcaciones_tienen_id_correcto(excel_prueba):
    """Verifica que el empleado_id se extrae bien de la columna 'ID'."""
    marcaciones = LectorExcel.leer_marcaciones(excel_prueba)
    ids_extraidos = {m.empleado_id for m in marcaciones}
    assert "EMP001" in ids_extraidos
    assert "EMP002" in ids_extraidos
    assert "EMP003" in ids_extraidos


# ── Prueba 3: El separador de punto y coma funciona ─────────────────────────
def test_horas_separadas_por_punto_y_coma(excel_prueba):
    """Verifica que las horas pegadas con ';' se separan correctamente."""
    marcaciones = LectorExcel.leer_marcaciones(excel_prueba)
    # Filtramos solo las marcas de EMP001 que debería tener exactamente 4
    marcas_emp001 = [m for m in marcaciones if m.empleado_id == "EMP001"]
    assert len(marcas_emp001) == 4
