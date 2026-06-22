import pytest
from datetime import date, time
from src.nucleo.modelos import Marcacion
from src.nucleo.procesador import ProcesadorAsistencia

def test_procesador_horas_trabajadas():
    # Arrange: Preparar datos
    procesador = ProcesadorAsistencia()
    marcas = [
        Marcacion("EMP-01", "Juan", date(2026, 6, 19), time(8, 0), "E"),
        Marcacion("EMP-01", "Juan", date(2026, 6, 19), time(12, 0), "S"),
        Marcacion("EMP-01", "Juan", date(2026, 6, 19), time(13, 0), "E"),
        Marcacion("EMP-01", "Juan", date(2026, 6, 19), time(17, 0), "S"),
    ]
    
    # Act: Ejecutar
    resultados = procesador.procesar(marcas)
    
    # Assert: Verificar
    assert len(resultados) == 1
    assert resultados[0].horas_trabajadas == 8.0
    assert resultados[0].tiene_novedad == False

def test_procesador_detecta_duplicados():
    procesador = ProcesadorAsistencia()
    marcas = [
        Marcacion("EMP-01", "Juan", date(2026, 6, 19), time(8, 0), "E"),
        Marcacion("EMP-01", "Juan", date(2026, 6, 19), time(8, 0), "E"), # Duplicado
    ]
    
    resultados = procesador.procesar(marcas)
    
    assert resultados[0].tiene_novedad == True
    assert any("EX-005" in nov for nov in resultados[0].novedades)