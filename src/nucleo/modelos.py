from dataclasses import dataclass, field # Decorador y fild configura el espacio para guardar los elementos
from datetime import date, time # Para guradar valeres tipo fecha y hora
from typing import Optional, List # Opcional es para un valor nulo o vaío

@dataclass #Decorador
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
