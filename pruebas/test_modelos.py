from datetime import date, time
from src.nucleo.modelos import Marcacion, RegistroDia

def test_crear_marcacion():
    """Verifica que el molde Marcacion se crea sin errores."""
    m = Marcacion("FH2148", "FH2148", date(2026,6,8), time(5,57,35), "ENTRADA")
    assert m.empleado_id == "FH2148"  # Si esto es falso, la prueba FALLA en rojo

def test_registro_sin_novedad_por_defecto():
    """Verifica que un día nuevo nace sin novedades."""
    r = RegistroDia("FH2148", "FH2148", date(2026,6,8))
    assert r.tiene_novedad == False
    assert r.novedades == []
