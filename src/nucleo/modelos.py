from dataclasses import dataclass, field
from datetime import date, time
from typing import Optional, List

@dataclass
class Marcacion:
    empleado_id: str
    nombre: str
    fecha: date
    hora: time
    tipo: str  

@dataclass
class RegistroDia:
    empleado_id: str
    nombre: str
    fecha: date
    entrada: Optional[time] = None
    inicio_almuerzo: Optional[time] = None
    fin_almuerzo: Optional[time] = None
    salida: Optional[time] = None
    horas_trabajadas: Optional[float] = None
    tiene_novedad: bool = False
    novedades: List[str] = field(default_factory=list)



"""

# ==========================================
# BLOQUE DE PRUEBA INDIVIDUAL
# ==========================================
if __name__ == '__main__':
    from datetime import date, time
    
    print("=== Prueba del Modelo Marcacion ===")
    # Creamos una marcación de prueba a mano (como si la leyéramos del Excel)
    marca = Marcacion(
        empleado_id="FH2148",
        nombre="FH2148",
        fecha=date(2026, 6, 8),
        hora=time(5, 57, 35),
        tipo="ENTRADA"
    )
    print(marca)
    
    print("\n=== Prueba del Modelo RegistroDia ===")
    # Creamos un registro de día con algunos datos
    registro = RegistroDia(
        empleado_id="FH2148",
        nombre="FH2148",
        fecha=date(2026, 6, 8),
        entrada=time(5, 57, 35),
        salida=time(14, 32, 8),
        horas_trabajadas=7.97,
        tiene_novedad=False
    )
    print(registro)
    
    print("\n=== Prueba de Novedad ===")
    # Simulamos un empleado que sí tiene problema
    registro_malo = RegistroDia(
        empleado_id="JL1898",
        nombre="JL1898",
        fecha=date(2026, 6, 8),
        entrada=time(5, 49, 5),
        tiene_novedad=True,
        novedades=["EX-003: Sin salida final detectada"]
    )
    print(f"¿Tiene novedad? {registro_malo.tiene_novedad}")
    print(f"Razón: {registro_malo.novedades}")
    
    print("\n✅ ¡Modelos funcionan perfectamente!")
"""